from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError

class ManufacturingOrder(models.Model):
    _inherit = 'product.product'

    product_subsidi = fields.Boolean('Product Subsidi')