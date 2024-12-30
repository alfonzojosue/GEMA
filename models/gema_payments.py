from odoo import models, fields, api
from odoo.exceptions import UserError
import logging

_logger = logging.getLogger(__name__)

class GemaPayments(models.Model):
    _name = 'gema.payments'
    _description = 'Gestión de Pagos de Contratos'

    name = fields.Char(string='Número de Pago', readonly=True, default='Nuevo')
    contract_id = fields.Many2one(
        'gema.contracts',
        string='Contrato Asociado',
        required=True,
        ondelete='cascade',
    )
    date = fields.Date(string='Fecha de Pago', default=fields.Date.today, required=True)
    amount = fields.Float(string='Monto Pagado', required=True)
    payment_method = fields.Selection(
        [('cash', 'Efectivo'), ('card', 'Tarjeta'), ('transfer', 'Transferencia')],
        string='Método de Pago',
        required=True,
    )
    state = fields.Selection(
        [('pending', 'Pendiente'), ('validated', 'Validado')],
        string='Estado',
        default='pending',
    )
    notes = fields.Text(string='Notas Adicionales')

    @api.model
    def create(self, vals):
        if vals.get('name', 'Nuevo') == 'Nuevo':
            vals['name'] = self.env['ir.sequence'].next_by_code('gema.payments') or 'Nuevo'
        return super(GemaPayments, self).create(vals)

    def action_validate_payment(self):
        """Valida el pago y actualiza el estado."""
        for record in self:
            if record.state != 'pending':
                raise UserError("Solo puedes validar pagos pendientes.")
            record.state = 'validated'

    def action_cancel_payment(self):
        """Cancela el pago y actualiza el estado."""
        for record in self:
            if record.state != 'pending':
                raise UserError("Solo puedes cancelar pagos pendientes.")
            record.state = 'cancelled'

