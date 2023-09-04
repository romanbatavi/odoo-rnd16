# -*- coding: utf-8 -*-
# from odoo import http


# class RmWebsite(http.Controller):
#     @http.route('/rm_website/rm_website', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/rm_website/rm_website/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('rm_website.listing', {
#             'root': '/rm_website/rm_website',
#             'objects': http.request.env['rm_website.rm_website'].search([]),
#         })

#     @http.route('/rm_website/rm_website/objects/<model("rm_website.rm_website"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('rm_website.object', {
#             'object': obj
#         })
