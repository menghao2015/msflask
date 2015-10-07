from threading import Thread
from flask import current_app, render_template
from flask.ext.mail import Message
from . import mail

def send_async_email(apl,msg):
	with apl.app_context():
		mail.send(msg)

def send_email(to, subject, template, **kwargs):
	apl = current_app._get_current_object()
#	msg = Message(app.config['FLASKY_MAIL_SUBJECT_PREFIX'] + ' ' + subject,
    		#	sender=app.config['FLASKY_MAIL_SENDER'], recipients=[to])

	msg = Message(apl.config['FLASKY_MAIL_SUBJECT_PREFIX'] + ' ' + subject,
			sender = apl.config['FLASKY_MAIL_SENDER'], recipients= [to])
	msg.body = render_template(template + '.txt', **kwargs)
	msg.html = render_template(template + '.html', **kwargs)

	thr = Thread(target=send_async_email, args=[apl,msg])
	thr.start()
	return thr



