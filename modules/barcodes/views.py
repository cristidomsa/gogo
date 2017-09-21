from flask import json, request
from flask_classy import route
from datetime import datetime
from pymongo.errors import PyMongoError

import calendar
import os

from modules.meta.views import gogoView
from modules.logging.controller import Logs

from modules.barcodes.controller import Barcodes

class barcodesView(gogoView):
	route_base = '/barcodes/'
	collection = 'barcodes'
	headers = ['name', 'content', 'img']
	templates = {'all': 'index_barcodes.html'}

	def make_content(self):

		content = {}


		if request.url.find('barcodes/scan') > -1:
			filename = request.args.get('filename')
			(t, d, q) = Barcodes.decode(filename).pop()
			content['string'] = d
			content['name'] = t
			content['path'] = filename

		else:
				
			content['string'] = request.json
			content['name'] = 'gen'

			content['path'] = 'code' + \
						 str(calendar.timegm(datetime.utcnow().utctimetuple())) + \
						 '.png'

			Barcodes.generate(content)

		return content

	@route('/scan/', endpoint='uploaded_file')
	def post(self):

		return super(barcodesView, self).post()

	def put(self):

		content = self.make_content()

		try:

			item_id = self.db.insert_one(content).inserted_id

			item = self.db.find_one({'_id': item_id}, {'_id': False})

			return json.jsonify({'inserted': {'content': item,
											 'date': datetime.now(),
											 'success': True,
											 'error': None}}), 206
		except PyMongoError as e:

			return json.jsonify({'inserted': {'content': content,
											 'date': datetime.now(),
											 'success': False,
											 'error': e.message}}), 409
	def after_put(self, response):

		resp_content = json.loads(response.response[0])['inserted']

		logged = Logs.insert({'datetime': resp_content['date'],
				'source': resp_content['content']['name'],
				'type': 'insert',
				'content': resp_content['content'],
				'status': 'OK' if resp_content['success'] else 'NOK',
				'error': resp_content['error']})

		return ("logged", 200) if logged else ("not logged", 400)
		