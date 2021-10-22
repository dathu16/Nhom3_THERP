from odoo import api, fields, models, _


class CallCard(models.Model):
    _name = 'call.card'
    _description = 'call.card'
    _rec_name = 'code'

    code = fields.Char(string='Số phiếu mượn', default="/")
    reader_id = fields.Many2one('res.partner', string='Tên độc giả', required=True)
    reader_code = fields.Char(string='Mã độc giả')
    start_date = fields.Date(string='Ngày mượn sách', default=lambda self: fields.Date.context_today(self), required=True)
    end_date = fields.Date(string='Ngày trả sách')
    due_date = fields.Date(string='Ngày đáo hạn')
    manager_id = fields.Many2one('hr.employee', string='Người xác nhận')
    description = fields.Text(string='Ghi chú mượn')
    return_note = fields.Text(string='Ghi chú trả')
    line_ids = fields.One2many('call.card.details', 'card_id', string='Chi tiết mượn')
    state = fields.Selection([
        ('confirmed', 'Đang mượn'),
        ('returned', 'Đã trả'),
        ('violate', 'Vi Phạm'),
    ], string='Trạng thái')

    @api.model
    def create(self, values):
        values['code'] = values.get('code') or '/'
        if values['code'].startswith('/'):
            values['code'] = (self.env['ir.sequence'].next_by_code('call.card') or '/') + values['code']
            values['code'] = values['code'][:-1] if values['code'].endswith('/') and values['code'] != '/' else values['code']
        values['state'] = 'confirmed'
        return super(CallCard, self).create(values)

    def action_confirm_return_book(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': _('Ghi chú'),
            'res_model': 'confirm.return.book.wizard',
            'view_mode': 'form',
            'context': {'ctx_call_card_id': self.id, 'default_call_card_id': self.id},
            'target': 'new',
        }

    def action_confirm_violate(self):
        self.ensure_one()
        pass


class CallCardDetails(models.Model):
    _name = 'call.card.details'
    _description = 'call.card.details'

    card_id = fields.Many2one('call.card', string='ID phiếu mượn sách')
    book_id = fields.Many2one('product.template', string='Tên sách', domain="[('is_book','=',True)]")
    book_code = fields.Char(string='Mã sách', related='book_id.default_code')
    publishing_company = fields.Char(string='Nhà xuất bản', related='book_id.publishing_company')
    description = fields.Text(string='Ghi chú')
