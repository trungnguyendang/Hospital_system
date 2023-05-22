from odoo import api, fields, models
from odoo.exceptions import ValidationError
class HospitalPatient(models.Model):
    _name = "hospital.patient"
    _inherit = 'mail.thread'
    _description = "hospital system"

    name = fields.Char(string='Name', required=True, tracking=True)
    age = fields.Integer(string="Age", tracking=True)
    is_child = fields.Boolean(string="Is Child?", tracking=True)
    gender = fields.Selection([('male', 'Male'), ('female', 'Female'), ('other', 'other')], string= "Gender", tracking=True)
    note = fields.Text(string="Note", tracking=True)
    capitalized_name = fields.Char(string="Capitalized Name", compute='_compute_capitalized_name', store=True)

    @api.model_create_multi
    def create(self, vals_list):
        return super(HospitalPatient,self).create(vals_list)

    @api.constrains('is_child', 'age')
    def _check_child_age(self):
        for patient in self:
            if patient.age ==0:
                raise ValidationError("Age has to be recorded! ")

    @api.depends('name')
    def _compute_capitalized_name(self):
        for patient in self:
            if patient.name:
                patient.capitalized_name = patient.name.upper()
            else:
                patient.capitalized_name = ''
    @api.onchange('age')
    def _onchange_age(self):
        if self.age <= 12:
            self.is_child = True
        else:
            self.is_child = False