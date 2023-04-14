# -*- coding: utf-8 -*-
# from odoo import http


# class RmPendataanWarga(http.Controller):
#     @http.route('/rm_pendataan_warga/rm_pendataan_warga', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/rm_pendataan_warga/rm_pendataan_warga/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('rm_pendataan_warga.listing', {
#             'root': '/rm_pendataan_warga/rm_pendataan_warga',
#             'objects': http.request.env['rm_pendataan_warga.rm_pendataan_warga'].search([]),
#         })

#     @http.route('/rm_pendataan_warga/rm_pendataan_warga/objects/<model("rm_pendataan_warga.rm_pendataan_warga"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('rm_pendataan_warga.object', {
#             'object': obj
#         })
