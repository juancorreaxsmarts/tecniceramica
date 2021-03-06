# -*- coding: utf-8 -*-
import logging
import datetime
import traceback
from dateutil.relativedelta import relativedelta
from odoo import fields, api, models, _

from odoo.tools import float_is_zero, float_compare, safe_eval, date_utils, email_split, email_escape_char, email_re
from odoo.tools.misc import formatLang, format_date, get_lang


_logger = logging.getLogger(__name__)

class TecniCeramicaStock(models.Model):
    _inherit = 'product.template'

    unidad = fields.Float(digits=(3,3))
    metros = fields.Float(digits=(3,3))
    cajas = fields.Float(digits=(3,3))



class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    unidad = fields.Float(string='Unidad', store=True,digits=(3,3))
    metros = fields.Float(string='Metros',store=True,digits=(3,3))
    cajas = fields.Float(string='Caja', store=True, digits=(3,3))
    #type = ields.selection()
    unidad_x = fields.Float(store=True) #compute='traerDatos' compute='_traer_datos_c',
    metros_x = fields.Float(store=True)
    cajas_x = fields.Float(store=True)

    #@api.depends('unidad_x', 'cajas_x')
#    def _traer_datos(self):
        #for line in self:
            #unidad = line.quantity/line.product_id.cajas*line.product_id.unidad
            #cajas = line.quantity/line.product_id.cajas
                #self.quantity = self.unidad*self.metros_x
            #return self.unidad

                #caja * unidad_x = unidad
                #metros / cajas_X = cajas
    #@api.depends('quantity')
    #def _traer_datos_c(self):
    #    for line in self.move_id:
    #        if line.type == "in_invoice":
    #            for i in self:
    #                if len(i.product_id):
    #                    self.unidad_x = i.product_id.unidad
    #                    self.metros_x = i.product_id.metros
    #                    self.cajas_x = i.product_id.cajas

    #                    self.unidad_c = self.quantity/self.cajas_x*line.unidad_x
    #                    self.cajas_c = self.quantity/self.cajas_x



class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    unidad = fields.Float(string='Unidad',default=1.0, store=True, digits=(3,3))
    metros = fields.Float(string='Metros',default=1.0, store=True, digits=(3,3))
    cajas = fields.Float(string='Caja',default=1.0, store=True, digits=(3,3))

    unidad_x = fields.Float(store=True) #compute='traerDatos'
    metros_x = fields.Float(store=True)
    cajas_x = fields.Float(store=True)

    @api.onchange('product_id', 'cajas', 'product_uom_qty')
    def _traer_datos(self):
        for line in self:
            if self.product_id:
                self.unidad_x = line.product_id.unidad
                self.metros_x = line.product_id.metros
                self.cajas_x = line.product_id.cajas

                self.unidad = self.cajas*self.unidad_x
                self.cajas = self.product_uom_qty/self.cajas_x
                #self.quantity = self.unidad*self.metros_x
            #return self.unidad

                #caja * unidad_x = unidad
                #metros / cajas_X = cajas
    def _prepare_invoice_line(self):
        res = super(SaleOrderLine, self)._prepare_invoice_line()
        res.update({
            #'quantity': self.product_uom_qty,
            'cajas': self.cajas,
            'unidad': self.unidad,

        })
        return res

class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    unidad = fields.Float(string='Unidad',default=1.0, store=True, digits=(3,3))
    cajas = fields.Float(string='Caja',default=1.0, store=True, digits=(3,3))

    unidad_x = fields.Float(store=True) #compute='traerDatos'
    metros_x = fields.Float(store=True)
    cajas_x = fields.Float(store=True)

    @api.onchange('product_id', 'cajas', 'product_qty')
    def _traer_datos(self):
        for line in self:
            if self.product_id:
                self.unidad_x = line.product_id.unidad
                self.metros_x = line.product_id.metros
                self.cajas_x = line.product_id.cajas

                self.unidad = self.cajas*self.unidad_x
                self.cajas = self.product_qty/self.cajas_x
                #self.quantity = self.unidad*self.metros_x
            #return self.unidad

                #caja * unidad_x = unidad
                #metros / cajas_X = cajas

    def _prepare_account_move_line(self, move):
        res = super(PurchaseOrderLine, self)._prepare_account_move_line(move)
        res.update({
        'cajas': self.cajas,
        'unidad': self.unidad,
        })
        return res
