from odoo import fields, models
from odoo.addons import decimal_precision as dp

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'
    
    loc_src_id = fields.Many2one('stock.location', string='Source Location', help="Config Source Location For Move Order", config_parameter="aa_move_order.loc_src_id")
    loc_dest_id = fields.Many2one('stock.location', string='Destination Location', help="Config Destination Location For Move Order", config_parameter="aa_move_order.loc_dest_id")