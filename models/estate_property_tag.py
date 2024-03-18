from odoo import fields,models,api

class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Estate Property Tag"
    _order = "name"
    name = fields.Char("Name", required=True)
    color = fields.Integer("Color")
    _sql_constraints = [('unique_tag', 'UNIQUE(name)', 'A property tag name must be unique')]