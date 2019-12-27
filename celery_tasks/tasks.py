from celery import Celery
from django.conf import settings
from django.core.mail import send_mail
import time

# for task worker
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dailyfresh.settings')
django.setup()


app = Celery('celery_tasks.tasks', broker='redis://192.168.2.15:6379/8')


@app.task
def send_register_active_email(to_email, username, token):
    subject = 'Dailyfresh Welcome'
    message = ''
    html_message = '<h1>%s, Welcome to Dailyfresh membership</h1> Please click the link to activate your account<br/><a href="http://127.0.0.1:8000/user/active/%s">http://127.0.0.1:8000/user/active/%s</a>' % (username, token, token)
    sender = settings.EMAIL_FROM
    recipient_list = [to_email]
    send_mail(subject, message, sender, recipient_list, html_message=html_message)
    time.sleep(5)
