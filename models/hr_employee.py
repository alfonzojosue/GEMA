from odoo import models, fields, api


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    is_teacher = fields.Boolean(string="Es profesor")
    subject_id = fields.Many2one('gema.subjects', string="Materia")