# -*- coding: utf-8 -*-
from django.http import HttpResponse, HttpResponseRedirect
from django.core.mail import BadHeaderError, send_mail


class Notifications:
    def send_email(self, paymentstatus):
        from_email = ''
        subject = 'ok'
        if paymentstatus == 'COMPLETE':
            message = 'success'
        else:
            message = 'unsuccess'
        send_mail(subject, message, from_email, ['ahmadi.zahra395@yahoo.com'])
        return send_mail(subject, message, from_email, ['ahmadi.zahra395@yahoo.com'])