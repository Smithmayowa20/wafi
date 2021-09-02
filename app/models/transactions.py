from __future__ import unicode_literals

from django.db import models
from django.core.mail import send_mail
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.db import models

from django.utils import timezone

from datetime import date

from decouple import config

from datetime import datetime, timedelta

from .user import Profile


class Transaction(models.Model):
    ADD = 'ADD'
    WITHDRAW = 'WDR'
    SEND = 'SEN'

    DOLLARS = 'USD'
    NAIRA = 'NGN'
    YUAN = 'YUA'
    YEN = 'YEN'

    TRANSACTION_CHOICES = (
        (ADD, 'Add'),
        (WITHDRAW, 'Withdraw'),
        (SEND, 'Send'),
    )

    CURRENCY_CHOICES = (
        (DOLLARS, 'Dollars'),
        (NAIRA, 'Naira'),
        (YUAN, 'Yuan'),
        (YEN, 'Yen'),
    )

    sender = models.ForeignKey('MyUser', on_delete=models.CASCADE, related_name='sender', null=True, blank=True)
    recipient = models.ForeignKey('MyUser', on_delete=models.CASCADE, related_name='recipient', null=True, blank=True)
    amount = models.CharField(_('transaction amount'), max_length=100,)
    transaction_type = models.CharField(max_length=3, choices=TRANSACTION_CHOICES, default=ADD, db_index=True)
    currency_type = models.CharField(max_length=3, choices=CURRENCY_CHOICES, default=DOLLARS, db_index=True)
    transaction_uuid = models.CharField(_('transaction uuid'),max_length=400, unique=True)
    created_date = models.DateTimeField(default=timezone.now, blank=True)

    def __unicode__(self):
        return '%s' % (self.transaction_uuid)


    def update_sender_balance(self, sender, amount):
        sender_profile = Profile.objects.get(user=sender)
        sender_profile.balance = int(sender_profile.balance) - float(amount)
        sender_profile.save()
        return sender_profile.balance


    def update_recipient_balance(self, recipient, amount):
        recipient_profile = Profile.objects.get(user=recipient)
        recipient_profile.balance = int(recipient_profile.balance) + float(amount)
        recipient_profile.save()
        return recipient_profile.balance