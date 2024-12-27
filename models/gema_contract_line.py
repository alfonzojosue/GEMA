import logging
from odoo import models, fields, api

# Configuración del logger
_logger = logging.getLogger(__name__)


class GemaContractLine(models.Model):
    _name = 'gema.contract.line'
    _description = 'Línea de Contrato'

    price = fields.Float(string='Precio', required=True, default=0.0)
    contract_id = fields.Many2one('gema.contracts', string='Contrato', required=True, ondelete='cascade')
    subject_id = fields.Many2one('gema.subjects', string='Materia', domain="[('id', 'in', allowed_subject_ids)]",)
    teacher_id = fields.Many2one('hr.employee', string="Profesor")


    allowed_subject_ids = fields.Many2many('gema.subjects', compute='_compute_allowed_subject_ids', string='Materias Permitidas')

    @api.model
    def create(self, vals):
        return super(GemaContractLine, self).create(vals)

    @api.depends('contract_id.student_id')
    def _compute_allowed_subject_ids(self):
        for line in self:
            if line.contract_id and line.contract_id.student_id:
                line.allowed_subject_ids = line.contract_id.student_id.subject_ids
            else:
                line.allowed_subject_ids = self.env['gema.subjects']

    @api.onchange('subject_id')
    def _onchage_teacher_id(self):
        if self.subject_id:
            return {
                'domain': {
                    'teacher_id': [('subject_id', '=', self.subject_id.id)],
                }
            }
        return {
            'domain': {
                'teacher_id': [],
            }
        }
