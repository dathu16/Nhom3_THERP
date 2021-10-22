from odoo import api, fields, models


class Shelve(models.Model):
    _name = 'shelve'
    _description = 'Shelve book'

    name = fields.Char(string='Tên kệ sách', required=True)
    active = fields.Boolean(string='Còn sử dụng', default=True)
    description = fields.Text(string='Mô tả')

    def action_inactive(self):
        self.write({'active': False})

    def action_active(self):
        self.write({'active': True})
