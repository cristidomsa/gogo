from flask import current_app
from modules.notifications.mail import send_mail

class Notifications():

	errors = {}

	@staticmethod
	def notify(error, name, date):
		
		if int(error) in Notifications.errors:
			send_mail(errors[int(error)], error, name, date)
