from datetime import datetime
import json
import math
# from typing_extensions import Required
from odoo.tools import float_round
from odoo import api, fields, models, _
from odoo.addons import decimal_precision as dp
from odoo.exceptions import UserError, RedirectWarning, ValidationError


class MoveOrder(models.Model):
    _name = 'move.order'
    _inherit = 'mail.thread'
    _order = 'create_date desc'

    name = fields.Char('Reference', default='/', readonly=True)
    date = fields.Date('Date', required=True, default=fields.Date.context_today, readonly=True, states={'draft': [('readonly', False)]}, track_visibility='onchange')
    user_id = fields.Many2one('res.users', string='Responsible', readonly=True, required=True, default=lambda self: self.env.user, copy=False)
    warehouse_id = fields.Many2one('stock.warehouse', 'Warehouse', required=True, readonly=True, states={'draft': [('readonly', False)]}, track_visibility='onchange')
    move_type_id = fields.Many2one('move.type', 'Type', domain="[('warehouse_id', '=', warehouse_id)]", readonly=True, states={'draft': [('readonly', False)]}, track_visibility='onchange')
    move_line = fields.One2many('move.order.line', 'move_id', 'Component Lines', readonly=True, states={'draft': [('readonly', False)]}, copy=True)
    loc_src_id = fields.Many2one('stock.location', string='Source Location', compute='_compute_get_loc_id', track_visibility='onchange', readonly=False, store=True)
    loc_dest_id = fields.Many2one('stock.location', string='Destination Location', compute='_compute_get_loc_id', track_visibility='onchange', readonly=False, store=True)
    # loc_src_id = fields.Many2one('stock.location', 'Source Location', track_visibility='onchange')
    # loc_dest_id = fields.Many2one('stock.location', 'Destination Location', track_visibility='onchange')
    picking_count = fields.Integer(string='Picking Count', compute='_get_picking')
    picking_line = fields.One2many('stock.picking', 'move_order_id', 'Picking Lines', readonly=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirm', 'Confirm'),
        ('done', 'Approved'),
        ('cancel', 'Cancel'),
    ], string='Status', readonly=True, copy=False, default='draft', track_visibility='onchange')
    partner_id = fields.Many2one('res.partner', string='Customer', track_visibility='onchange')
    note = fields.Text(string='Note')
    active = fields.Boolean(string='Active', default=True, track_visibility='onchange')
    domain_partner = fields.Char(compute='_compute_domain_partner', string='Domain Partner')

    move_order_type = fields.Selection([
        ('internal_move', 'Internal Move'),
        ('internal_use', 'Intenal Use'),
        ('physical_inventory', 'Physical Inventory')
    ], string='Move Order Type')
    physical_inventory_type = fields.Selection([
        ('adjust_in', 'Adjust In'),
        ('adjust_out', 'Adjust Out')
    ], string='Physical Inventory Type')
    description = fields.Char('Description')
    account_id = fields.Many2one('account.account', string='Account')
    
    @api.depends('physical_inventory_type')
    def _compute_get_loc_id(self):
        for mv in self:
            mv.loc_src_id = False
            mv.loc_dest_id = False
            if mv.physical_inventory_type == 'adjust_in':
                config_settings = mv.env['res.config.settings'].create({})
                mv.loc_src_id = config_settings.loc_src_id
            if mv.physical_inventory_type == 'adjust_out':
                config_settings = mv.env['res.config.settings'].create({})
                mv.loc_dest_id = config_settings.loc_dest_id
    
    @api.depends('warehouse_id')
    def _compute_domain_partner(self):
        for o in self:
            partner_ids = self.env['res.partner'].search([('customer', '=', True), ('warehouse_ids', 'in', o.warehouse_id.ids)])
            o.domain_partner = json.dumps([('id', 'in', partner_ids.ids)])

    @api.model
    def create(self, vals):
        nama = '/'
        if vals['move_order_type'] == 'physical_inventory':
            nama = self.env['ir.sequence'].next_by_code('physical.inventory')
        elif vals['move_order_type'] == 'internal_use':
            nama = self.env['ir.sequence'].next_by_code('internal.use')
        else:
            nama = self.env['ir.sequence'].next_by_code('move.order')
        vals['name'] = nama
        return super(MoveOrder, self).create(vals)

    def unlink(self):
        for o in self:
            if o.state != 'draft':
                raise UserError(("Move Order tidak bisa dihapus pada state %s !") % (o.state))
        return super(MoveOrder, self).unlink()

    @api.onchange('move_type_id')
    def onchange_move_type_id(self):
        if self.move_type_id:
            self.loc_src_id = self.move_type_id.loc_src_id.id
            self.loc_dest_id = self.move_type_id.loc_dest_id.id

    def move_draft(self):
        for o in self:
            return o.write({'state': 'draft'})

    def move_open(self):
        for o in self:
            return o.write({'state': 'confirm'})

    def dict_picking(self):
        res = {
            'origin': self.name,
            'move_type': 'one',
            'location_id': self.loc_src_id.id,
            'location_dest_id': self.loc_dest_id.id,
            'partner_id': self.partner_id.id,
            'picking_type_id': self.warehouse_id.int_type_id.id,
            'move_order_id': self.id,
        }
        return res

    def move_done(self):
        obj_picking = self.env['stock.picking']
        obj_move = self.env['stock.move']

        for o in self:
            if not o.move_line:
                raise UserError(("Silahkan mengisi tabel Components Lines !"))
            # if not o.is_pass_through:
            if o.move_line:
            # PICKING MATERIALS
                picking_raw_id = obj_picking.create(o.dict_picking())
                for l in o.move_line:
                    move_raw = obj_move.create({
                        'name': l.product_id.partner_ref,
                        'product_id': l.product_id.id,
                        'product_uom_qty': l.product_qty,
                        'product_uom': l.inventory_uom.id,
                        'picking_id': picking_raw_id.id,
                        'location_id': o.loc_src_id.id,
                        'location_dest_id': o.loc_dest_id.id,
                        'procure_method': 'make_to_stock',
                        'move_order_line_id': l.id,
                        'origin': o.name,
                        'warehouse_id': o.warehouse_id.id,
                    })
                picking_raw_id.action_confirm()
                picking_raw_id.action_assign()
            return o.write({'state': 'done'})

    @api.depends('picking_line')
    def _get_picking(self):
        for x in self:
            x.update({
                'picking_count': len(set(x.picking_line.ids)),
            })

    def action_view_picking(self):
        picking_ids = self.mapped('picking_line')
        action = self.env.ref('stock.action_picking_tree_all').read()[0]
        if len(picking_ids) > 1:
            action['domain'] = [('id', 'in', picking_ids.ids)]
        elif len(picking_ids) == 1:
            form_view = [(self.env.ref('stock.view_picking_form').id, 'form')]
            if 'views' in action:
                action['views'] = form_view + [(state, view) for state, view in action['views'] if view != 'form']
            else:
                action['views'] = form_view
            action['res_id'] = picking_ids.ids[0]
        else:
            action = {'type': 'ir.actions.act_window_close'}
        return action

    def action_update_onhand_line(self):
        for o in self:
            for line in o.move_line:
                line._compute_onhand_qty()

class MoveOrderLine(models.Model):
    _name = 'move.order.line'

    move_id = fields.Many2one('move.order', 'MO Reference', required=True, ondelete='cascade')
    product_id = fields.Many2one('product.product', 'Product', required=True)
    categ_id = fields.Many2one('product.category', string='Product Category', related='product_id.categ_id', store=True)
    product_uom = fields.Many2one('uom.uom', 'UoM')
    inventory_uom = fields.Many2one('uom.uom', 'UoM')
    onhand_qty = fields.Float('Source Onhand Qty', digits_compute=dp.get_precision('Product UoM'), compute='_compute_onhand_qty', store=True)
    dest_onhand_qty = fields.Float('Dest. Onhand Qty', digits_compute=dp.get_precision('Product UoM'), compute='_compute_onhand_qty', store=True)
    product_qty = fields.Float('Request Qty', digits_compute=dp.get_precision('Product UoM'))

    locator = fields.Char('Locator')
    qty_diff = fields.Float('Qty Diff')

    @api.onchange('onhand_qty','product_qty')
    def _onchange_qty_diff_const(self):
        for line in self:
            line.qty_diff = line.product_qty - line.onhand_qty
            for move in line.move_id:
                if move.physical_inventory_type == 'adjust_out' and line.onhand_qty and line.product_qty:
                    if line.onhand_qty < line.product_qty:
                        raise ValidationError('if physical inventory type is adjust out, then field qty before cannot smaller than qty after!')
                if move.physical_inventory_type == 'adjust_in' and line.onhand_qty and line.product_qty:
                    if line.onhand_qty > line.product_qty:
                        raise ValidationError('if physical inventory type is adjust in, then field qty after cannot smaller than qty before!')
    
    @api.constrains('onhand_qty','product_qty')
    def _constrains_qty(self):
        for line in self:
            for move in line.move_id:
                if move.physical_inventory_type == 'adjust_out' and line.onhand_qty and line.product_qty:
                    if line.onhand_qty < line.product_qty:
                        raise ValidationError('if physical inventory type is adjust out, then field qty before cannot smaller than qty after!')
                if move.physical_inventory_type == 'adjust_in' and line.onhand_qty and line.product_qty:
                    if line.onhand_qty > line.product_qty:
                        raise ValidationError('if physical inventory type is adjust in, then field qty after cannot smaller than qty before!')
    
    @api.onchange('product_id', 'product_uom', 'inventory_uom')
    def product_id_change(self):
        if self.product_id:
            self.inventory_uom = self.product_id.uom_id.id
    
    @api.depends('product_id')
    def _compute_onhand_qty(self):
        for o in self:
            if o.product_id and o.move_id and o.move_id.loc_src_id:
                onhand = sum(o.product_id.stock_quant_ids.filtered(lambda x: x.location_id.id == o.move_id.loc_src_id.id).mapped('quantity'))
                o.onhand_qty = onhand
            else:
                o.onhand_qty = 0

            if o.product_id and o.move_id and o.move_id.loc_dest_id:
                onhand = sum(o.product_id.stock_quant_ids.filtered(lambda x: x.location_id.id == o.move_id.loc_dest_id.id).mapped('quantity'))
                o.dest_onhand_qty = onhand
            else:
                o.dest_onhand_qty = 0

class MoveType(models.Model):
    _name = 'move.type'

    name = fields.Char('Name', required=True)
    warehouse_id = fields.Many2one('stock.warehouse', 'Warehouse', required=True)
    loc_src_id = fields.Many2one('stock.location', 'Source Location', domain="[('warehouse_id', '=', warehouse_id), ('usage', '=', 'internal')]", required=True)
    loc_dest_id = fields.Many2one('stock.location', 'Destination Location', domain="[('id', '!=', loc_src_id), ('usage', '!=', 'view')]", required=True)

    @api.onchange('warehouse_id')
    def onchange_warehouse(self):
        if self.warehouse_id:
            if not self.warehouse_id.location_ids:
                raise UserError("Data warehouse belum diupdate, silahkan klik button 'Update WH Location' di Form Warehouse %s" % self.warehouse_id.name)


class Location(models.Model):
    _inherit = 'stock.location'

    warehouse_id = fields.Many2one('stock.warehouse', 'Warehouse', store=True)

class Warehouse(models.Model):
    _inherit = "stock.warehouse"

    loc_kitchen_id = fields.Many2one('stock.location', 'Kitchen Location', domain="[('usage', '=', 'internal')]", readonly=False, store=True)
    location_ids = fields.One2many('stock.location', 'warehouse_id', string="Location")

    def update_warehouse_location(self):
        for wh in self:
            if wh.loc_kitchen_id:
                wh.loc_kitchen_id.warehouse_id = wh.id
                wh.lot_stock_id.warehouse_id = wh.id
                if not wh.loc_kitchen_id.active:
                    wh.loc_kitchen_id.active = True

class StockPicking(models.Model):
    _inherit = 'stock.picking'

    move_order_id = fields.Many2one('move.order', 'MO Reference', ondelete='cascade')

class StockMove(models.Model):
    _inherit = 'stock.move'

    move_order_line_id = fields.Many2one('move.order.line', 'MO Line Reference', ondelete='cascade')
