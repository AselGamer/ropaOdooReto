
# -*- coding:utf-8 -*-
from odoo import fields, models, api
from odoo.exceptions import UserError
import logging
logger = logging.getLogger(__name__)


class Compra(models.Model):
    _name = 'compra'

    numero_compra = fields.Char(string='Numero compra', copy=False)
    name = fields.Char(string='Nombre', related='numero_compra', readonly=True)
    fecha_compra = fields.Date(string='Fecha compra', copy=False, default=fields.Date.today())
    currency_id = fields.Many2one(comodel_name='res.currency', string='Moneda', default=lambda self: self.env.company.currency_id.id)
    comprador_id = fields.Many2one(comodel_name='res.partner', string='Comprador')
    categoria_comprador_id = fields.Many2one(
        comodel_name='res.partner.category',
        string='Categoria comprador',
        default=lambda self: self.env['res.partner.category'].search([('name', '=', 'Comprador')]))
    base = fields.Monetary(String='Base Indisponible')
    impuestos = fields.Monetary(String='Impuestos', compute='_compute_total')
    total = fields.Monetary(string='Total', compute='_compute_total')
    detalle_ids = fields.One2many(comodel_name='compra.detalle', inverse_name='compra_id', string='Detalle')
    state = fields.Selection(
        selection=[('borrador', 'Borrador'), ('realizada', 'Realizada')],
        default='borrador', string='Estado', copy=False
    )
    arr_ropa = []

    @api.model
    def create(self, variables):
        sequence = self.env['ir.sequence']
        correlativo = sequence.next_by_code('sequencia.compra')
        variables['numero_compra'] = correlativo
        variables['state'] = 'realizada'
        return super(Compra, self).create(variables)

    @api.depends('detalle_ids')
    def _compute_total(self):
        for record in self:
            sub_total = 0
            for linea in record.detalle_ids:
                sub_total += linea.importe
            record.base = sub_total
            record.impuestos = sub_total * 0.21
            record.total = sub_total * 1.21


class DetalleCompra(models.Model):
    _name = 'compra.detalle'

    compra_id = fields.Many2one(comodel_name='compra', string='Compra')
    ropa_id = fields.Many2one(comodel_name='ropa', string='Ropa')
    name = fields.Char(string='Nombre', related='ropa_id.name', readonly=True)
    image = fields.Binary(string='Imagen', related='ropa_id.image', readonly=True)
    descripcion = fields.Text(string='Descripcion', related='ropa_id.descripcion', readonly=True)
    cantidad = fields.Integer(string='Cantidad', default=1, attrs={'min': 0})
    precio = fields.Float(string='Precio', related='ropa_id.precio', readonly=True)
    importe = fields.Monetary(string='Importe')

    currency_id = fields.Many2one(comodel_name='res.currency', string='Moneda', related='ropa_id.currency_id')

    @api.onchange('cantidad', 'precio')
    def _compute_importe(self):
        for record in self:
            if record.cantidad > record.ropa_id.stock or record.cantidad < 0:
                record.cantidad = 0
            record.importe = record.cantidad * record.precio
    @api.onchange('ropa_id')
    def _onchange_ropa_id(self):
        for record in self:
            if record.ropa_id:
                if record.ropa_id.stock <= 0:
                    raise UserError('No se puede comprar una ropa sin stock')
                if record.ropa_id.id in record.compra_id.arr_ropa:
                    raise UserError('No se puede comprar dos veces la misma ropa')
                record.compra_id.arr_ropa.append(record.ropa_id.id)

    @api.model
    def create(self, variables):
        ropa = self.env['ropa'].browse(variables['ropa_id'])

        if not ropa:
            raise UserError('No se puede crear una linea de compra sin ropa')

        if variables['cantidad'] <= 0:
            raise UserError('No se puede crear una linea de compra sin cantidad')

        if variables['cantidad'] > ropa.stock:
            raise UserError('No se puede crear una linea de compra con una cantidad mayor al stock')

        ropa.stock -= variables['cantidad']
        return super(DetalleCompra, self).create(variables)