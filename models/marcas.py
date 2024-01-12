# -*- coding:utf-8 -*-

from odoo import models, fields, api


class Marcas(models.Model):
    _name = 'ropa.marcas'

    name = fields.Char('Nombre', required=True)
    image = fields.Binary('Imagen')