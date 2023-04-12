from odoo import api, fields, models, _

class SaleOrder(models.Model):
    _inehrit = 'sale.order'

    def create_mo(self):
        obj_mo = self.env['mrp.production']
        obj_bom = self.env['mrp.bom']
        for line in self.order_line:
            bom_fg = obj_bom._bom_find(line.product_id)
            if bom_fg:
                if not bom_fg.manual_mo:
                    mo_fg = obj_mo.create({
                                        'product_tmpl_id': line.product_template_id.id,
                                        'product_qty': line.product_uom_qty, # ambil dari QTY SO
                                        'product_uom_id': line.product_uom.id,
                                        })
                    mo_fg._onchange_product_id()
                    faktor = line.product_uom_qty / bom_fg.product_qty
                    for bom_line in bom_fg.bom_line_ids:
                        bom_wip = obj_bom._bom_find(bom_line.product_id)
                        if bom_wip:
                            if not bom_wip.manual_mo:
                                mo_wip = obj_mo.create({
                                        'product_tmpl_id': bom_line.product_id.product_template_id.id,
                                        'product_qty': bom_line.product_uom_qty * faktor,
                                        'product_uom_id': line.product_uom.id,
                                        })
                                mo_wip._onchange_product_id()
