import requests

from flask import json, render_template, request, current_app, redirect, url_for
from flask_classy import route
from datetime import datetime

from modules.meta.views import gogoView

class itemsView(gogoView):
	route_base = '/items/'
	collection = 'items'
	headers = ['name','order', 'error', 'processed', 'status']
	templates = {'all': 'index.html'}

	@route('/feed_table_data/')
	def add_table(self):

		#return json.jsonify(os.getcwd())
		with open('./assets/table.json', 'r') as f:
			content = json.load(f)
			try: 
				items = [self.db.replace_one({"name": item['name']}, item, True) for item in content['items']]
			except:
				return "Unexpected error:"
				#TODO: add error message
					
		return redirect("http://localhost:5000/items/", code=302)

	@route('/plot/')
	def plot(self):
		#label = request.json['label']
		#value = request.json['value']

		label = 'order'
		value = 'error'

		output = [(r[label], r[value]) for r in self.db.find()]
		return render_template('chart.html',
								#condition=name + '=' + str(value),
								#title=self.collection,
								#user='demo',
								labels=[x for  (x,_) in output],
								values=[y for  (_,y) in output])