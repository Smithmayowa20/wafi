from functools import wraps
from django.http import HttpResponseRedirect
from app.models import (
    Transaction, Profile,
)


def has_enough_balance(function):
    @wraps(function)
    def wrap(request, *args, **kwargs):

        try:
            profile = Profile.objects.get(user=request.user)
        except Profile.DoesNotExist:
            return HttpResponseRedirect('/')

        amount = request.GET.get('amount', None)

        if (int(profile.balance) >= int(amount)):
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