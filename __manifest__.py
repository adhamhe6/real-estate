# -*- coding: utf-8 -*-
{
'name': "Real Estate",
'description': """
Demo excercise in Odoo documentation """,
'author': "Adham",
'version': '0.1',
'category': "Real Estate/Brokerage",
'depends': ['base'],
'data': [
    'security/security.xml',
    'security/security_rules.xml',
    'security/ir.model.access.csv',
    'report/estate_property_template.xml',
    'report/estate_property_by_saleperson_template.xml',
    'report/estate_property_reports.xml',
    'views/estate_property_views.xml',
    'views/estate_property_offer_views.xml',
    'views/estate_property_type_views.xml',
    'views/estate_propetty_tag_views.xml',
    'views/estate_menus.xml',
    'views/res._users_views.xml',
    'demo/estate.property.type.csv',
    'demo/estate_property_demo_data.xml',
    'demo/estate_property_demo_data_base_on_partner.xml',
    'demo/estate_property_demo_data_x2many_field.xml',
],
'demo':[
    'demo/estate.property.type.csv',
    'demo/estate.property.tag.csv',
    'demo/estate_property_demo_data.xml',
    'demo/estate_property_demo_data_base_on_partner.xml',
    'demo/estate_property_demo_data_x2many_field.xml',
],
'sequence': 1,
'installable': True,
'application': True
}