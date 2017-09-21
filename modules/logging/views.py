from modules.meta.views import gogoView

class logsView(gogoView):
	route_base = '/logs/'
	collection = 'logs'
	headers = ['datetime', 'source', 'type', 'content', 'status', 'error']
	templates = {'all': 'index_logs.html'}

	def a(self):
		pass