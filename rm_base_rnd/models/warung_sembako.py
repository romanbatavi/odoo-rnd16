from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError

class WarungSembako(models.Model):
    _name = 'warung.sembako'
    _description = 'Warung Sembako'
    
    partner_id = fields.Many2one('res.partner', string='Pembeli')
    date = fields.Date('Tanggal', default=fields.Date.today())
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

    @api.onchange('standard_price')
    def _onchange_standard_price(self):
        self.qty == 0
        if self.standard_price:
            self.total = self.standard_price * self.qty

    @api.onchange('product_id')
    def _onchange_product_id(self):
        self.product_id == False
        if self.product_id:
            self.standard_price = self.product_id.standard_price
