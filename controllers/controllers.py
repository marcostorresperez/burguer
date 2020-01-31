# -*- coding: utf-8 -*-
from odoo import http

# class Burguer(http.Controller):
#     @http.route('/burguer/burguer/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/burguer/burguer/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('burguer.listing', {
#             'root': '/burguer/burguer',
#             'objects': http.request.env['burguer.burguer'].search([]),
#         })

#     @http.route('/burguer/burguer/objects/<model("burguer.burguer"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('burguer.object', {
#             'object': obj
#         })