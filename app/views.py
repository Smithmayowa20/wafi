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

    if uuid:
        transaction = Transaction.objects.create(
            recipient = recipient_user,
            sender = request.user,
            transaction_type = 'SEN',
            transaction_uuid = uuid,
	    )

        transaction.update_sender_balance(request.user,amount)
        transaction.update_recipient_balance(recipient_user,amount)

        response_data['status'] = True
        response_data['message'] = 'Transaction Created Successfully'

    return JsonResponse(response_data)


@login_required
def add_money(request):
    response_data = {}

    uuid = request.GET.get('uuid', None)
    amount = request.GET.get('amount', None)
    recipient = request.user

    if uuid:
        transaction = Transaction.objects.create(
            recipient = recipient,
            transaction_type = 'ADD',
            transaction_uuid = uuid,
	    )

        transaction.update_recipient_balance(recipient, amount)

        response_data['status'] = True
        response_data['message'] = 'Transaction Created Successfully'

    return JsonResponse(response_data)


@login_required
@has_enough_balance
def withdraw_money(request):
    response_data = {}

    uuid = request.GET.get('uuid', None)
    amount = request.GET.get('amount', None)

    if uuid:
        transaction = Transaction.objects.create(
            sender = request.user,
            transaction_type = 'WTH',
            transaction_uuid = uuid,
	    )

        transaction.update_sender_balance(request.user,amount)

        response_data['status'] = True
        response_data['message'] = 'Transaction Created Successfully'

    return JsonResponse(response_data)


@login_required
def check_balance(request):
    response_data = {}

    profile = Profile.objects.get(user=request.user)
    balance = profile.balance

    response_data['balance'] = balance

    return JsonResponse(response_data)



@login_required
def create_profile(request):
    response_data = {}

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
        user=request.user,
    )

    response_data['status'] = True
    response_data['message'] = 'User Profile Created Successully'

    return JsonResponse(response_data)