# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo import tools
from odoo.tools.translate import _

class ProductRequestInherit(models.Model):
    _name = "product.request.inherit"
    _inherit = 'vit.product.request.line'

    # product_id = fields.Many2one(comodel_name='product.product', string='Product')

    # @api.multi
     def create_pr(self, product_id, request_line=None):
        cr=self.env.cr
        purchase_requisition  = self.env['purchase.requisition']
        product_request       = self.env['vit.product.request']
        product_req = self.env['vit.product.request.line']
        origins = product_request.browse(request_line['origins'])

        line_department_ids = []
        for x in request_line['qty_per_dept'].keys():
            line_department_ids.append( (0,0,{
                'qty':1,
                'request_id':request_line['qty_per_dept'][x]['request_id'],
                'warehouse_id':request_line['qty_per_dept'][x]['warehouse_id'],
                'department_id': self.department_id.id}) )

#