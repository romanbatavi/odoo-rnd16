# -*- coding: utf-8 -*-
# from odoo import http


# class RmBaseRnd(http.Controller):
#     @http.route('/rm_base_rnd/rm_base_rnd', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/rm_base_rnd/rm_base_rnd/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('rm_base_rnd.listing', {
#             'root': '/rm_base_rnd/rm_base_rnd',
#             'objects': http.request.env['rm_base_rnd.rm_base_rnd'].search([]),
#         })

#     @http.route('/rm_base_rnd/rm_base_rnd/objects/<model("rm_base_rnd.rm_base_rnd"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('rm_base_rnd.object', {
#             'object': obj
#         })
