# -*- coding: utf-8 -*-

from odoo import models, fields, api

class MasterKecamatan(models.Model):
    _name = 'master.kecamatan'
    _description = 'Master Kecamatan'

    nama_kecamatan = fields.Char('Kode kecamatan')
    nama_kota = fields.Selection([
        ('jakarta_timur', 'Jakarta Timur'),
        ('jakarta_barat', 'Jakarta Barat'),
        ('jakarta_selatan', 'Jakarta Selatan'),
        ('jakarta_utara', 'Jakarta Utara'),
        ('jakarta_pusat', 'Jakarta Pusat'),
    ], string='Nama Kota')
