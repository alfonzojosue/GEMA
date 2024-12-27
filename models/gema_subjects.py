from odoo import models, fields, api


class GemaSubjects(models.Model):
    _name = 'gema.subjects'
    _description = 'Modelo de materias'

    name = fields.Char(string='Materia', required=True)
    code = fields.Char(string='Codigo', help="Codigo unico, identificador de la materia")
    description = fields.Text(string='Descripcion')
    credits = fields.Integer(string='Creditos', required=True, default=0,)
    state = fields.Selection(
        [('active', 'Activo'), ('inactive', 'Inactivo')],
        string='Estado',
        default='active',
        required=True,
    )
    teacher_id = fields.Many2one(
        'hr.employee',
        string='Profesor',
        domain=[('is_teacher', '=', True)],
        required=True,
    )
