from odoo import fields,models,api

class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Estate Property Type"
    _order = "sequence,name"
    name = fields.Char(required=True)
    property_ids = fields.One2many('estate.property', 'property_type_id')
    offer_ids = fields.One2many('estate.property.offer', 'property_type_id')
    offer_count = fields.Integer(compute='_compute_offer_count')
    sequence = fields.Integer('Sequence')
    _sql_constraints = [('unique_type', 'UNIQUE(name)', 'A property type name must be unique')]

    @api.depends('offer_ids')
    def _compute_offer_count(self):
        for r in self:
            r.offer_count = len(r.offer_ids)