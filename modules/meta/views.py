from flask import json, render_template, request, redirect
from flask_classy import FlaskView, route
from pymongo.errors import PyMongoError
from datetime import datetime
from exceptions import ValueError

from modules.logging.controller import Logs
from modules.notifications.controller import Notifications

class gogoView(FlaskView):

	db = None
	collection = None
	templates = {}

	def make_content(self):
		return request.json

	def index(self):
		output = self.db.find()

		return render_template(self.templates['all'],
								condition='all',
								title=self.collection,
								user='Demo',
								headers=self.headers,
								items=output)

	def get(self, name, value):

		try: 
			value = int(value)
		except ValueError:
			pass
		output = self.db.find({name: value})

		return render_template(self.templates['all'],
								condition=name + ' == ' + str(value),
								title=self.collection,
								user='Demo',
								headers=self.headers,
								items=output)

	def post(self):

		content = self.make_content()

		try: 
			
			print content 
			item_id = self.db.insert_one(content).inserted_id

			item = self.db.find_one({'_id': item_id}, {'_id': False})

			return json.jsonify({'inserted': {'content': item,
											'success': True,
											'date': datetime.now(),
											'error': None}}), 201
		except PyMongoError as e:

			if '_id' in content:
				del content['_id']
			return json.jsonify({'inserted': {'content': content,
											'success': False,
											'date': datetime.now(),
											'error': e.message}}), 409

	def after_post(self, response):

		resp_content = json.loads(response.response[0])['inserted']

		logged = Logs.insert({'datetime': resp_content['date'],
				'source': resp_content['content']['name'],
				'type': 'insert',
				'content': resp_content['content'],
				'status': 'OK' if resp_content['success'] else 'NOK',
				'error': resp_content['error']})
		if 'error' in resp_content['content']:
			notify = Notifications.notify(resp_content['content']['error'],
											resp_content['content']['name'],
											resp_content['date'])

		return ("logged", 200) if logged else ("not logged", 400)

	def put(self):

		content = self.make_content()

		try:

			item = self.db.update_one({"name": content['name']}, {'$set': content}, True)


			return json.jsonify({'updated': {'content': content,
											 'date': datetime.now(),
											 'success': True,
											 'error': None}}), 206

		except PyMongoError as e:

			return json.jsonify({'updated': {'content': content,
											 'date': datetime.now(),
											 'success': False,
											 'error': e.message}}), 409

	def after_put(self, response):

		resp_content = json.loads(response.response[0])['updated']

		logged = Logs.insert({'datetime': resp_content['date'],
				'source': resp_content['content']['name'],
				'type': 'update',
				'content': resp_content['content'],
				'status': 'OK' if resp_content['success'] else 'NOK',
				'error': resp_content['error']})

		return ("logged", 200) if logged else ("not logged", 400)
		
	def delete(self, name, value):

		try: 
			value = int(value)
		except ValueError:
			pass

		result = self.db.delete_many({name: value})

		output = self.db.find()

		return json.jsonify({'deleted': {'content': {name: value},
										 'date': datetime.now(),
										 'success': result.deleted_count,
										 'error': ''}}), 200

	def after_delete(self, response):

		resp_content = json.loads(response.response[0])['deleted']

		logged = Logs.insert({'datetime': resp_content['date'],
				'source': resp_content['content'],
				'type': 'delete',
				'content': resp_content['success'],
				'status': 'OK',
				'error': resp_content['error']})

		return ("logged", 200) if logged else ("not logged", 400)
