import re

from odoo import models,fields,api
from odoo.exceptions import UserError,ValidationError
from dateutil.relativedelta import relativedelta

class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate Property"
    _order = "id desc"

    name = fields.Char("Title", required=True)
    description = fields.Text("Description")
    postcode = fields.Char("Postcode")
    date_availability = fields.Date("Available From", copy=False, default=fields.Date.today()+relativedelta(months=3))
    expected_price = fields.Float("Expected Price", required=True)
    selling_price = fields.Float("Selling Price", readonly=True, copy=False)
    bedrooms = fields.Integer("Bedrooms", default=2)
    living_area = fields.Integer("Living Area (sqm)")
    facades = fields.Integer("Facades")
    garage = fields.Boolean("Garage")
    garden = fields.Boolean("Garden")
    garden_area = fields.Integer("Garden Area (sqm)")
    garden_orientation = fields.Selection(string="Garden Orientation", selection=[('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')])
    active = fields.Boolean(default=True)
    state = fields.Selection(selection=[('new', 'New'), ('received', 'Offer Received'), ('accepted', 'Offer Accepted'), ('sold', 'Sold'), ('canceled', 'Canceled')],
                             copy=False, required=True, default='new')
    property_type_id = fields.Many2one('estate.property.type', string="Property Type")
    buyer_id = fields.Many2one('res.partner', string="Buyer", copy=False)
    salesman_id = fields.Many2one('res.users', string="Salesman")
    tag_ids = fields.Many2many('estate.property.tag')
    offer_ids = fields.One2many('estate.property.offer', 'property_id')
    total_area = fields.Integer("Total Area (sqm)", compute="_total_area")
    best_price = fields.Float("Best Offer", compute="_compute_best_price",store=True)

    _sql_constraints = [('positive_expected_price', 'CHECK(expected_price > 0)', 'Expected price must be strictly positive!'),
                        ('positive_selling_price', 'CHECK(selling_price >= 0)', 'Selling price must be positive')]
    @api.constrains('selling_price','expected_price')
    def _check_selling_price(self):
        for r in self:
            if r.selling_price and r.selling_price < 0.9 * r.expected_price:
                    raise ValidationError('The selling price cannot be lower than 90% of the expected price')
    @api.depends("living_area","garden_area")
    def _total_area(self):
        for r in self:
            r.total_area = r.living_area + r.garden_area

    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for r in self:
            r.best_price = max(r.offer_ids.mapped("price"), default=None)

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = None
            self.garden_orientation = None

    @api.model
    def unlink(self):
        for r in self:
            if r.state == 'new' or r.state == 'canceled':
                return super().unlink()
            else:
                raise UserError('Cannot delete property if it state is not new or canceled')

    def make_property_sold(self):
        if self.state == 'canceled':
            raise UserError('Cancel properties cannot be sold')
        else:
            self.state = 'sold'
        return True

    def make_property_cancel(self):
        if self.state == 'sold':
            raise UserError('Sold properties cannot be canceled')
        else:
            self.state = 'canceled'
        return True
