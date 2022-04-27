# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import datetime
from mongoengine import Document, EmbeddedDocument, fields


class Shoppings(EmbeddedDocument):
    paidAt = fields.DateTimeField(
        default=datetime.datetime.now, editable=False,
    )
    payment_status = fields.StringField(max_length=255)
    amount = fields.IntField(max_length=255)
    orderId = fields.StringField(max_length=255)


class Feature(EmbeddedDocument):
    email_address = fields.EmailField(verbose_name="Email")
    customer_numberphone = fields.IntField(max_length=13)


class NotificationStatus(EmbeddedDocument):
    sent_at = fields.DateTimeField(
        default=datetime.datetime.now, editable=False,
    )
    status = fields.StringField(max_length=255)


class Notif(EmbeddedDocument):
    email = fields.ListField(
        fields.EmbeddedDocumentField('NotificationStatus'), blank=True,
    )
    sms = fields.ListField(
        fields.EmbeddedDocumentField('NotificationStatus'), blank=True,
    )


class Payment(Document):
    customer_numberphone = fields.IntField(max_length=13,  primary_key=True)
    features = fields.EmbeddedDocumentField('Feature', blank=True,)
    notifications = fields.ListField(
        fields.EmbeddedDocumentField('Notif'), blank=True,
    )
    shopping_list = fields.ListField(fields.EmbeddedDocumentField('Shoppings', blank=True,)
                                     )