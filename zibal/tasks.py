from zibal.models import NotificationStatus

from celery import shared_task
from django.core.mail import BadHeaderError, send_mail
# from push_notifications.gcm import send_message
from django.contrib import messages

from datetime import timedelta

@shared_task
def send_email_task(paymentstatus):
    from_email = ''
    subject = 'ok'
    if paymentstatus == 'COMPLETE':
        message = 'success'
    else:
        message = 'unsuccess'
    # send_mail(subject, message, from_email, ['ahmadi.zahra395@gmail.com'])
    return send_mail(subject, message, from_email, ['ahmadi.zahra395@gmail.com'], fail_silently=False)


