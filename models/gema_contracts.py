from odoo import models, fields, api
import uuid
import base64
import logging

_logger = logging.getLogger(__name__)

class GemaContracts(models.Model):
    _name = 'gema.contracts'
    _desctription = 'Modelo de contrato de los estudiantes'

    name = fields.Char('Codigo del contrato')
    total_amount = fields.Float(
        string='Costo del contrato',
        compute='_compute_total_amount',
    )
    state = fields.Selection(
        [
            ('draft', 'Por revisar'),
            ('confirmed', 'Confirmado'),
            ('cancelled', 'Cancelado')
        ],
        string='Estado',
        default='draft',
    )
    total_paid = fields.Float(
        string='Total Pagado',
        compute='_compute_total_paid',
        store=True,
    )
    student_id = fields.Many2one(
        'res.partner',
        string='Estudiante',
        required=True,
        domain=[('type_person', '=', 'student')],
    )
    subject_ids = fields.Many2many(
        'gema.subjects',
        'gema_contract_subject_rel',
        'contract_id',
        'subject_id',
        string='Materia',
    )
    line_ids = fields.One2many('gema.contract.line', 'contract_id', string='Materias')
    invoice_id = fields.Many2one(
        'account.move',
        string='Factura Asociada',
    )
    product_id = fields.Many2one(
        'product.product',
        string='Producto del Contrato',
        readonly=True,
    )

    payment_ids = fields.One2many('gema.payments', 'contract_id', string='Pagos Asociados')

    attachment_ids = fields.One2many(
        'ir.attachment',
        'res_id',
        string='Adjuntos',
        domain=[('res_model', '=', 'gema.contracts')]
    )


    @api.depends('payment_ids')
    def _compute_total_paid(self):
        for contract in self:
            contract.total_paid = sum(payment.amount for payment in contract.payment_ids)
            if contract.total_paid >= contract.total_amount and contract.state != 'confirmed':
                contract.approve_contract()

    @api.model
    def create(self, vals):
        """Sobrescribe el método create para asignar un código único hexadecimal."""
        vals['name'] = uuid.uuid4().hex[:15].upper()

        # Crear un producto de tipo servicio para el contrato
        product_vals = {
            'name': f"Contrato {vals.get('name')}",
            'type': 'service',
            'list_price': vals.get('total_amount', 0.0),
        }
        product = self.env['product.product'].create(product_vals)

        vals['product_id'] = product.id  # Asociamos el producto al contrato
        return super(GemaContracts, self).create(vals)

    @api.depends('line_ids')
    def _compute_total_amount(self):
        """Calcula el total del precio del contrato"""
        for contract in self:
            contract.total_amount = sum(subject.price for subject in contract.line_ids)

    def approve_contract(self):
        """Funcion para la aprobacion y creacion de un reporte con las
        materias inscrita"""
        self.state = 'confirmed'
        self.create_invoice()
        report = self.env.ref('GEMA.report_gema_contract')
        report_ref = 'GEMA.report_gema_contract'
        res_ids = [self.id]
        report_content, _ = report._render(report_ref, res_ids)
        attachment = self.env['ir.attachment'].create({
            'name': "Contrato",
            'datas': base64.b64encode(report_content),
            'res_model': 'gema.contracts',
            'res_id': self.id,
            'type': 'binary',
        })
        return attachment

    def create_invoice(self):
        """Crea una factura asociada al contrato"""
        if not self.student_id:
            raise ValueError("El contrato debe tener un estudiante asociado")

        # Crear una factura de venta
        invoice_vals = {
            'move_type': 'out_invoice',
            'partner_id': self.student_id.id,
            'invoice_date': fields.Date.today(),
            'invoice_line_ids': [(0, 0, {
                'product_id': self.product_id.id,
                'quantity': 1,
                'price_unit': self.total_amount,
            })],
        }

        invoice = self.env['account.move'].create(invoice_vals)
        self.invoice_id = invoice.id

        return invoice

    def action_view_payments(self):
        """Acción para abrir la vista de pagos asociados a un contrato."""
        return {
            'type': 'ir.actions.act_window',
            'name': 'Pagos del Contrato',
            'view_mode': 'tree,form',
            'res_model': 'gema.payments',
            'domain': [('contract_id', '=', self.id)],
            'context': {'default_contract_id': self.id},
        }

