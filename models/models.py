# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo import tools
import time
import logging
from odoo.tools.translate import _
from collections import defaultdict
from odoo.exception import UserError

class ProductRequestInherit(models.Model):
    _name = "product.request.inherit"
    _inherit = ['vit.product.request.line','vit.product.request']

    product_qty = fields.Many2one(comodel_name='',string="Quantity")

    @api.multi


#