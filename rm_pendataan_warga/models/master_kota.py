# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class rm_pendataan_warga(models.Model):
#     _name = 'rm_pendataan_warga.rm_pendataan_warga'
#     _description = 'rm_pendataan_warga.rm_pendataan_warga'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
