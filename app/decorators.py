from functools import wraps
from django.http import HttpResponseRedirect
from app.models import (
    Transaction, Profile,
)

from app.utils.helper import currency_conversion

def has_enough_balance(function):
    @wraps(function)
    def wrap(request, *args, **kwargs):

        try:
            profile = Profile.objects.get(user=request.user)
        except Profile.DoesNotExist:
            return HttpResponseRedirect('/')

        amount = request.GET.get('amount', None)
        transaction_currency = request.GET.get('currency', None)

        profile_default_balance = int(profile.balance)
        default_currency = profile.default_currency

        transaction_value = currency_conversion(transaction_currency, default_currency, amount)

        if (profile_default_balance >= transaction_value):
            return function(request, *args, **kwargs)
        else:
            return HttpResponseRedirect('/')

    return wrap


def can_perform_transaction(function):
    @wraps(function)
    def wrap(request, *args, **kwargs):

        try:
            profile = Profile.objects.get(user=request.user)
            return HttpResponseRedirect('/')
        except Client.DoesNotExist:
            return function(request, *args, **kwargs)

    return wrap