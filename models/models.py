# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo import tools
from odoo.tools.translate import _

class ProductRequestInherit(models.Model):
    _name = "vit.product.request"
    _inherit = "vit.product.request"
    
    def action_create_pr_baru(self):
        cr = self.env.cr
        purchase_requisition          = self.env['purchase.requisition']
        purchase_requisition_line      = self.env['purchase.requisition.line']   
        line_department_ids = []
        line_department_ids.append( (0,0,{
            'qty':1,
            'request_id':self.id,
            'warehouse_id':self.warehouse_id.id,
            'department_id': self.department_id.id}) )
 
        for prd_req in self:
            pr_line_ids = []
            for lines in prd_req.product_request_line_ids:
                pr_line_ids.append( (0,0,{
                    'product_id'    : lines.product_id.id,
                    'description'    : lines.name,
                    'product_qty'    : lines.product_qty,
                    'product_uom_id': lines.product_uom_id.id,
                    'schedule_date'    : lines.date_required,
                    'line_department_ids': line_department_ids
                }) )
            partner = False
            if prd_req.partner_id:
                partner=self.partner_id.id
            pr_id = purchase_requisition.create({
                'name'            : self.env['ir.sequence'].get('purchase.requisition.purchase.tender'),
                'exclusive'        : 'exclusive',
                'warehouse_id'      : self.warehouse_id.id ,
                'line_ids'         : pr_line_ids,
                'partner_id'        : partner,
                'origin'          : prd_req.name
            })
            #update state dan pr_id di line product request asli
            cr.execute("update vit_product_request_line set state=%s, purchase_requisition_id=%s where product_request_id = %s",
             ( 'onprogress', pr_id.id,  prd_req.id  ))

            self.write({'state':'onprogress'}, )

            body = _("PR bid created")
            self.send_followers()

            return pr_id


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
                'request_id':self.origin.id,
                'warehouse_id':self.warehouse_id.id,
                'department_id': self.department_id.id}) )
    
    