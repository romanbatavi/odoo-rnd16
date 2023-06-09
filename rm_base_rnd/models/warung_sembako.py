from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError

class WarungSembako(models.Model):
    _name = 'warung.sembako'
    _description = 'Warung Sembako'
    
    partner_id = fields.Many2one('res.partner', string='Pembeli')
    date = fields.Date('Tanggal', default=fields.Date.today())
    tipe_sembako = fields.Selection([
        ('subsidi', 'Subsidi'),
        ('general', 'General')
    ], string='Tipe Sembako')
    # KEY
    sembako_line = fields.One2many('barang.sembako', 'sembako_id', string='Komponen')

class BarangSembako(models.Model):
    _name = 'barang.sembako'
    _description = 'Sembako'

    # KEY
    sembako_id = fields.Many2one('warung.sembako', string='Sembako ID')
    # COMPONENTS
    product_id = fields.Many2one('product.product', string='Produk')
    standard_price = fields.Monetary('Harga')
    qty = fields.Float('Kuantiti')
    total = fields.Float('Total')
    currency_id = fields.Many2one('res.currency', string='Currency')
    # REL
    tipe_sembako_rel = fields.Selection([
        ('subsidi', 'Subsidi'),
        ('general', 'General')
    ], string='Tipe Sembako', related='sembako_id.tipe_sembako')

    @api.onchange('tipe_sembako_rel')
    def _onchange_prod_id(self):
        if self.tipe_sembako_rel == 'general':
            return {"domain": {'product_id':[]}}
        else:
            return {"domain": {'product_id':[('product_subsidi', '=', True)]}}

    @api.onchange('standard_price','qty')
    def _onchange_standard_price(self):
        self.qty == 0
        if self.standard_price:
            self.total = self.standard_price * self.qty

    @api.onchange('product_id')
    def _onchange_product_id(self):
        self.product_id == False
        if self.product_id:
            self.standard_price = self.product_id.standard_price
