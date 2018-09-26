from flask_mail import Message
from threading import Thread
from flask import render_template, current_app
from . import mail


def send_mail(to, subject, template, **kwargs):
    app = current_app._get_current_object()
    msg = Message(app.config['FLASKY_MAIL_SUBJECT_PREFIX'] + ' ' + subject,
                  sender=app.config['FLASKY_MAIL_SENDER'], recipients=[to])

    # msg = Message(current_app.config.FLASKY_MAIL_SUBJECT_PREFIX + subject,
    #               sender=current_app.config.FLASKY_MAIL_SENDER, recipients=[to])
    msg.body = render_template(template + ".txt", **kwargs)
    msg.html = render_template(template + ".html", **kwargs)

    thr = Thread(target=send_async_mail, args=[app, msg])
    thr.start()

    return thr


def send_async_mail(app, msg):
    with app.app_context():
        mail.send(msg)
