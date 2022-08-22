# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __manifest__.py file in module root
# directory
##############################################################################
from odoo import models, fields, api
from odoo.exceptions import UserError,ValidationError
from datetime import datetime
import requests

class ResCurrency(models.Model):
	_inherit = 'res.currency'

	@api.model
	def update_dolarsi(self):
		dolarsi_url = self.env['ir.config_parameter'].get_param('dolarsi_url')
		if not dolarsi_url:
			raise UserError('No esta presente URL de Bluelytics')
		try:
			res = requests.get(dolarsi_url)
		except:
			raise UserError('No se pudo obtener tipo de cambio')
		if res.status_code != 200:
			raise UserError('No se pudo obtener tipo de cambio')
		data = res.json()
		if type(data) == list:
			data = data[0]
		try:
			value = data.get('casa').get('venta')
			value = float(value.replace(',','.'))
		except:
			raise UserError('No se puede determinar tipo de cambio')
		currency_id = self.search([('name','=','USD')])
		if currency_id:
			vals = {
				'name': str(datetime.now())[:10],
				'currency_id': currency_id.id,
				'rate': 1 / value
				}
			rate = self.env['res.currency.rate'].search([('currency_id','=',currency_id.id),('name','=',str(datetime.now())[:10])])
			if not rate:
				return_id = self.env['res.currency.rate'].create(vals)
