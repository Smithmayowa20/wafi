from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

# Create your views here.


from app.models import ( 
	MyUser, Transaction,
    Profile,
)

from app.decorators import (
    has_enough_balance,
)

from app.utils.helper import currency_conversion

from django.http import HttpResponse, JsonResponse

from datetime import datetime, timedelta

from decouple import config


@login_required
@has_enough_balance
def send_money(request):
    response_data = {}
    recipient_email = request.GET.get('recipient_email',None)

    try:
        recipient_user = MyUser.objects.get(email=recipient_email)

    except MyUser.DoesNotExist:
        response_data['status'] = False
        response_data['message'] = 'Recipient User Does Not Exist'
        return JsonResponse(response_data)

    uuid = request.GET.get('uuid', None)
    amount = request.GET.get('amount', None)
    currency = request.GET.get('currency', None)

    recipient_profile = Profile.objects.get(user=recipient_user)
    recipient_default_currency = recipient_profile.default_currency
    recipient_transaction_value = currency_conversion(currency,recipient_default_currency,amount)

    sender_profile = Profile.objects.get(user=request.user)
    sender_default_currency = sender_profile.default_currency
    sender_transaction_value = currency_conversion(currency,sender_default_currency,amount)


    if uuid:
        transaction = Transaction.objects.create(
            recipient = recipient_user,
            sender = request.user,
            transaction_type = 'SEN',
            transaction_uuid = uuid,
            currency_type = currency,
	    )

        transaction.update_sender_balance(request.user,sender_transaction_value)
        transaction.update_recipient_balance(recipient_user,recipient_transaction_value)

        response_data['status'] = True
        response_data['sender_balance'] = sender_profile.balance
        response_data['recipient_balance'] = recipient_profile.balance
        response_data['message'] = 'Transaction Created Successfully'

    return JsonResponse(response_data)


@login_required
def add_money(request):
    response_data = {}

    uuid = request.GET.get('uuid', None)
    amount = request.GET.get('amount', None)
    currency = request.GET.get('currency', None)
    recipient = request.user

    profile = Profile.objects.get(user=request.user)
    default_currency = profile.default_currency

    transaction_value = currency_conversion(currency,default_currency,amount)
    
    if uuid:
        transaction = Transaction.objects.create(
            recipient = recipient,
            transaction_type = 'ADD',
            transaction_uuid = uuid,
            currency_type = currency,
	    )

        transaction.update_recipient_balance(recipient, transaction_value)

        response_data['status'] = True
        response_data['recipient_balance'] = profile.balance
        response_data['message'] = 'Transaction Created Successfully'

    return JsonResponse(response_data)


@login_required
@has_enough_balance
def withdraw_money(request):
    response_data = {}

    uuid = request.GET.get('uuid', None)
    amount = request.GET.get('amount', None)
    currency = request.GET.get('currency', None)
    sender = request.user

    profile = Profile.objects.get(user=request.user)
    default_currency = profile.default_currency

    transaction_value = currency_conversion(currency,default_currency,amount)

    if uuid:
        transaction = Transaction.objects.create(
            sender = request.user,
            transaction_type = 'WTH',
            transaction_uuid = uuid,
            currency_type = currency,
	    )

        transaction.update_sender_balance(sender, transaction_value)

        response_data['status'] = True
        response_data['sender_balance'] = profile.balance
        response_data['message'] = 'Transaction Created Successfully'

    return JsonResponse(response_data)


@login_required
def check_balance(request):
    response_data = {}

    profile = Profile.objects.get(user=request.user)
    balance = profile.balance
    default_currency = profile.default_currency

    response_data['balance'] = balance
    response_data['currency'] = default_currency

    return JsonResponse(response_data)



@login_required
def create_profile(request):
    response_data = {}

    first_name = request.POST.get('first_name', None)
    last_name = request.POST.get('last_name', None)
    middle_name = request.POST.get('middle_name', None)
    bank_name = request.POST.get('bank_name', None)
    account_number = request.POST.get('account_number', None)
    account_name = request.POST.get('account_name', None)
    phone_number = request.POST.get('phone_number', None)
    home_address = request.POST.get('home_address', None)
    country = request.POST.get('country', None)
    balance = request.POST.get('balance', None)
    default_currency = request.POST.get('default_currency', None)

	
    profile = Profile.objects.create(
        first_name = first_name,
        last_name = last_name,
        middle_name = middle_name,
        bank_name = bank_name,
        account_number = account_number,
        account_name = account_name,
        phone_number = phone_number,
        home_address = home_address,
        country = country,
        default_currency = default_currency,
        balance = balance,
        user=request.user,
    )

    response_data['first_name'] = profile.first_name
    response_data['balance'] = profile.balance
    response_data['default_currency'] = profile.default_currency
    response_data['status'] = True
    response_data['message'] = 'User Profile Created Successfully'

    return JsonResponse(response_data)