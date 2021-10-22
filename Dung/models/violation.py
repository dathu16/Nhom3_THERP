from datetime import date
from odoo import api, fields, models


class Violation(models.Model):
    _name = 'violation'
    _description = 'violation'

    name = fields.Char(string='Mã vi phạm', default='/')
    reader_id = fields.Many2one('res.partner', string='Tên độc giả', required=True)
    call_card_id = fields.Many2one('call.card', string='Số Phiếu mượn', required=True)
    handler_id = fields.Many2one(
        'hr.employee', string='Người xử lý',
        default=lambda self: self.env['hr.employee'].search([('user_id', '=', self._uid)]), limit=1,
        required=True
    )
    reason = fields.Text(string='Lý do vi phạm', required=True)
    comment = fields.Text(string='Ghi chú')
    violation_date = fields.Date(
        string='Ngày vi phạm', default=lambda self: fields.Date.context_today(self),
        required=True
    )
    violation_money = fields.Monetary(string='Tiền vi phạm (phải đòng)', digits=(16, 0))
    state = fields.Selection([
        ('draft', 'Mới'),
        ('inprogress', 'Đang xử lý'),
        ('done', 'Đã xử lý'),
        ('closed', 'Đóng'),
    ])
    currency_id = fields.Many2one('res.currency', default=lambda self: self.env.ref('base.VND'))
    date_of_rov = fields.Date(string='Ngày tiếp nhận xử lý')
    date_done = fields.Date(string='Ngày hoàn thành xử lý')

    def action_start_to_inprogress(self):
        self.write({'state': 'inprogress', 'date_of_rov': date.today()})

    def action_done(self):
        self.write({'state': 'done', 'date_done': date.today()})

    def action_close(self):
        self.write({'state': 'closed'})

    @api.model
    def create(self, values):
        values['name'] = values.get('name') or '/'
        if values['name'].startswith('/'):
            values['name'] = (self.env['ir.sequence'].next_by_code('violation') or '/') + values['name']
            values['name'] = values['name'][:-1] if values['name'].endswith('/') and values['name'] != '/' else values['name']
        values['state'] = 'draft'
        return super(Violation, self).create(values)
