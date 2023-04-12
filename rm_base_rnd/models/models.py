# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class rm_base_rnd(models.Model):
#     _name = 'rm_base_rnd.rm_base_rnd'
#     _description = 'rm_base_rnd.rm_base_rnd'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
