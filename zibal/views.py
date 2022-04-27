# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
import mongoengine

from .models import Payment, Feature, Shoppings
from .zibal_gateway import zibal
from .tasks import send_email_task

# from .notifications import Notifications

_payment_url = 'https://gateway.zibal.ir/start/{}'
mongoengine.connect(db='onlineshopping', host='127.0.0.1')


class StartBuying:

    @staticmethod
    def start(response):
        return render(response, "Cardpay.html")

    def Card(self, request):
        self.refNumber = request.POST.get('refNumber')
        self.email = request.POST.get('email')
        self.amount = request.POST.get('amount')
        order_id = request.POST.get('order_id')
        response = zibal().request(self.amount, order_id, self.refNumber, None, None)
        self.insert_database()
        if response['result'] == 100:
            return redirect(_payment_url.format(str(response['trackId'])))
        else:
            result = 'مبلغ تراکنش کمتر از حد مجاز است'
            return render(request, 'Result.html', {'result': result})

    def verify(self, request):
        trackId = request.GET['trackId']
        order_id = request.GET['orderId']
        verify_response = zibal().verify(trackId)
        if verify_response['result'] == 100 and verify_response['status'] == 1:
            paymentstatus = 'COMPLETE'
        else:
            paymentstatus = 'Cancel by user'
        email_status = send_email_task(paymentstatus)
        self.update_database(order_id, paymentstatus, email_status)
        return render(request, 'Result.html', {'result': paymentstatus})

    def insert_database(self):
        features = Feature(email_address=self.email, customer_numberphone=self.refNumber)
        # shopping_list = Shoppings(amount=amount, orderId=order_id)
        insert = Payment(customer_numberphone=self.refNumber, features=features)
        insert.save()

    def update_database(self, order_id, paymentstatus, email_status):
        # print(self.amount)
        category = Shoppings()
        category.payment_status = paymentstatus
        # category.amount = self.amount
        category.orderId = order_id
        update_dict = {
            'push__shopping_list': paymentstatus
        }
        # shopping_list = Shoppings(payment_status=paymentstatus)
        article = Payment.objects.with_id(self.refNumber)
        article.update(**update_dict)
        article.save()
