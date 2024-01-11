# -*- coding:utf-8 -*-

from odoo import models, fields, api

class Ropa(models.Model):
    _name = 'ropa'

    name = fields.Char(string="Nombre", required=True)
    descripcion = fields.Text(string="Descripcion")
    currecy_id = fields.Many2one(comodel_name='res.currency', string="Moneda", default=lambda self: self.env.company.currency_id.id)
    precio = fields.Monetary(string="Precio", currency_field='currecy_id')
    stock = fields.Integer(string="Stock")
    imagen = fields.Binary(string="Imagen")
    vista_imagen = fields.Binary(string="Imagen Vista", related='imagen', readonly=True)
    marca_id = fields.Many2one(comodel_name='ropa.marcas', string="Marca")
    imagen_marca = fields.Binary(related='marca_id.image', string='Imagen Marca')
    talla = fields.Selection(selection=[('S', 'S'), ('M', 'M'), ('L', 'L'), ('XL', 'XL')], string="Talla")
