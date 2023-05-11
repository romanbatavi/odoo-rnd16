# -*- coding: utf-8 -*-

from odoo import models, fields, api

class MasterKota(models.Model):
    _name = 'master.kota'
    _description = 'Master Kota'

    nama_kota = fields.Char('Nama Kota')
    selection = fields.Selection([
        ('jakarta_timur', 'Jakarta Timur'),
        ('jakarta_barat', 'Jakarta Barat'),
        ('jakarta_selatan', 'Jakarta Selatan'),
        ('jakarta_utara', 'Jakarta Utara'),
        ('jakarta_pusat', 'Jakarta Pusat'),
    ], string='Nama Kota')
