# -*- coding: utf-8 -*-

import requests


class zibal:
    merchant = "zibal"
    callback_url = "http://127.0.0.1:8000/callbackurl"

    def __init__(self):
        self._verify_api_url = 'https://gateway.zibal.ir/v1/verify'
        self._payment_url = 'https://gateway.zibal.ir/start/{}'

    def request(self, amount, order_id, mobile, description, multiplexingInfos = None):
        data = {}
        data['merchant'] = self.merchant
        data['callbackUrl'] = self.callback_url
        data['amount'] = amount

        data['orderId'] = order_id
        data['refNumber'] = mobile
        data['description'] = description
        data['multiplexingInfos'] = multiplexingInfos
        response = self.postTo('request', data)
        return response

    def verify(self, trackId):
        data = {}
        data['merchant'] = self.merchant
        data['trackId'] = trackId
        verify_response =  self.postTo('verify', data)
        return verify_response

    def postTo(self, path, parameters):
        url = "https://gateway.zibal.ir/v1/" + path
        response = requests.post(url = url, json= parameters)
        return response.json()
