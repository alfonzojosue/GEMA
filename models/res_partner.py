from odoo import models, fields


class ResPartner(models.Model):
    _inherit = 'res.partner'

    last_name = fields.Char(string="Apellido")
    type_person = fields.Selection([
        ('student', 'Estudiante'),
        ('teacher', 'Profesor'),
        ('administrative', 'Administrativo')], string="Tipo de persona")
    
    subject_ids = fields.Many2many(
        'gema.subjects',
        string='Materia',
    )

