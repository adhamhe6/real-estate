from odoo import fields,models,api
from odoo.exceptions import UserError
from dateutil.relativedelta import relativedelta

class EstatePropertyOffer(models.Model):
    _name="estate.property.offer"
    _description="Estate Property Offer"
    _order = "price desc"
    price = fields.Float("Price")
    partner_id = fields.Many2one('res.partner', string="Partner", required=True)
    status = fields.Selection(string="Status", selection=[('refused', 'Refused'), ('accepted', 'Accepted')], copy=False)
    property_id = fields.Many2one('estate.property', required=True, ondelete="cascade")
    property_type_id = fields.Many2one(related='property_id.property_type_id', store=True)
    validity = fields.Integer(string="Validity (days)", default=7)
    date_deadline = fields.Date(string="Deadline", compute='_compute_date_deadline', inverse='_inverse_date_deadline')

    _sql_constraints = [('positive_price', 'CHECK(price > 0)', 'An offer price must be strictly positive!')]
    @api.depends('create_date', 'validity')
    def _compute_date_deadline(self):
        for r in self:
            if r.create_date:
                r.date_deadline = (r.create_date + relativedelta(days=r.validity)).date()
    @api.model
    def create(self, vals):
        property = self.env['estate.property'].browse(vals['property_id'])
        if vals['price'] < property.best_price:
                raise UserError("Cannot create offer with a lower amount than an existing offer")
        property.state = 'received'
        return super().create(vals)
    def _inverse_date_deadline(self):
        for r in self:
            if r.create_date and r.date_deadline:
                r.validity = (r.date_deadline - r.create_date.date()).days

    def make_accept(self):
        for r in self:
            # Neu da accepted offer thi k cho accept offer nua
            # if 'accepted' in r.property_id.offer_ids.mapped('status'):
            #     raise UserError('Can only accept one offer!')
            offers = r.property_id.offer_ids - r
            for offer in offers:
                offer.make_refuse()
            r.status = 'accepted'
            r.property_id.state='accepted'
            r.property_id.selling_price = r.price
            r.property_id.buyer_id = r.partner_id
        return True

    def make_refuse(self):
        for r in self:
            r.status = 'refused'
        # Neu k co offer nao duoc accepted thi reset selling price va buyer
        if 'accepted' not in r.property_id.offer_ids.mapped('status'):
            r.property_id.selling_price = None
            r.property_id.buyer_id = None
            r.property_id.state = 'received'
        return True