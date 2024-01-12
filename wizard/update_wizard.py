# -*- coding:utf-8 -*-
from odoo import fields, models, api


class UpdateDateWizard(models.TransientModel):
    _name = 'update.wizard.date'

    name = fields.Date(string='Nueva Fecha')

    def update_fecha_compra(self):
        compra_obj = self.env['compra']
        compra_obj = compra_obj.browse(self._context['active_id'])
        compra_obj.fecha_compra = self.name