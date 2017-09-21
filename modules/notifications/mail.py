from mailer import Mailer, Message
from flask import current_app



templates = {'error': {'subject': 'Error occured on Demo platform',
					   'html': """The error <strong>{error}</strong> occured on <strong>{name}</strong> at <strong>{date}</strong>. Action needed.""",
					   'body': """This is alternate text."""},
			'warning': {'subject': 'Warning occured on Demo platform',
					   'html': """The warning <strong>{error}</strong> occured on <strong>{name}</strong> at <strong>{date}</strong>. Please revise.""",
					   'body': """This is alternate text."""},
			'info': {'subject': 'Info on Demo platform',
					   'html': """The info <strong>{error}</strong> occured on <strong>{name}</strong> at <strong>{date}</strong>.""",
					   'body': """This is alternate text."""}}				   


def send_mail(severity, error, name, date):
	message = Message(From="platform@demo.com",
                  To=templates[severity]['dest'],
                  Subject=templates[severity]['subject'])
	message.Body = templates[severity]['html'].format(error=error, name=name, date=date)
	#message.attach("file.jpg")

	sender = Mailer('mail.demo.com')
	sender.send(message)
