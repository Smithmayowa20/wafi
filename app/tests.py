from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse

from app.models import Profile, Transaction

import json

# Create your tests here.
USER_MODEL = get_user_model()


class TestTransactionModelAndView(TestCase):
    """
    Things to test:
    - Test all transaction types
	- Test login_required view decorator
    """

    @classmethod
    def setUpTestData(cls):
        cls.client = Client()
        cls.url_1 = reverse('add_money')
        cls.url_2 = reverse('send_money')
        cls.url_3 = reverse('withdraw_money')

        cls.user = USER_MODEL.objects.create_user(
            email='johndoe@test.com',
            first_name='John',
            last_name='Doe',
            password='password456'
        )
        cls.user_2 = USER_MODEL.objects.create_user(
            email='sarahabigaile@test.com',
            first_name='Sarah',
            last_name='Abigail',
            password='password123'
        )
        cls.profile = Profile.objects.create(
            first_name='John',
            last_name='Doe',
            user=cls.user,
            balance='50000',
		)
        cls.profile_2 = Profile.objects.create(
            first_name='Sarah',
            last_name='Abigail',
            user=cls.user_2,
            balance='70000',
		)
        cls.add_transaction_type = Transaction.objects.create(
            recipient=cls.user,
            amount='5000',
            transaction_uuid='Ref472749204',
            transaction_type='ADD',
        )
        cls.send_transaction_type = Transaction.objects.create(
            recipient=cls.user,
            amount='6000',
            transaction_uuid='Ref678749204',
            transaction_type='SEN',
        )
        cls.wth_transaction_type = Transaction.objects.create(
            recipient=cls.user,
            amount='7000',
            transaction_uuid='Ref0977749204',
            transaction_type='WTH',
        )


    def test_create_user(self):
        """ Tests that a user object has been created with this email"""

        self.assertEqual(self.user.email, 'johndoe@test.com')

        self.assertEqual(self.user_2.email, 'sarahabigaile@test.com')

    def test_create_profile(self):
        """ Tests that a profile object has been created with this first_name && user foreign field"""

        self.assertEqual(self.profile.first_name, 'John')
        self.assertEqual(self.profile.last_name, 'Doe')
        self.assertEqual(self.profile.balance, '50000')
        self.assertEqual(self.profile.user, self.user)

        self.assertEqual(self.profile_2.first_name, 'Sarah')
        self.assertEqual(self.profile_2.last_name, 'Abigail')
        self.assertEqual(self.profile_2.balance, '70000')
        self.assertEqual(self.profile_2.user, self.user_2)


    def test_create_add_transaction(self):
        """ Tests that an add transaction object has been created with this uuid, amount and transaction type"""

        self.assertEqual(self.add_transaction_type.amount, '5000')
        self.assertEqual(self.add_transaction_type.transaction_uuid, 'Ref472749204')
        self.assertEqual(self.add_transaction_type.transaction_type, 'ADD')
        self.assertEqual(self.add_transaction_type.recipient, self.user)

    def test_create_send_transaction(self):
        """ Tests that a send transaction object has been created with this uuid, amount and transaction type"""

        self.assertEqual(self.send_transaction_type.amount, '6000')
        self.assertEqual(self.send_transaction_type.transaction_uuid, 'Ref678749204')
        self.assertEqual(self.send_transaction_type.transaction_type, 'SEN')
        self.assertEqual(self.send_transaction_type.recipient, self.user)

    def test_create_wth_transaction(self):
        """ Tests that a withdraw transaction object has been created with this uuid, amount and transaction type"""

        self.assertEqual(self.wth_transaction_type.amount, '7000')
        self.assertEqual(self.wth_transaction_type.transaction_uuid, 'Ref0977749204')
        self.assertEqual(self.wth_transaction_type.transaction_type, 'WTH')
        self.assertEqual(self.wth_transaction_type.recipient, self.user)

    
    def test_user_must_be_logged_in(self):
        """ Tests that a non-logged in user is redirected """

        response_1 = self.client.get(self.url_1)
        self.assertEqual(response_1.status_code, 302)

        response_2 = self.client.get(self.url_2)
        self.assertEqual(response_2.status_code, 302)

        response_3 = self.client.get(self.url_3)
        self.assertEqual(response_3.status_code, 302)


    def test_all_transaction_views(self):
        """ Tests all transaction types with a logged in user and make sure they  get a 200 status code on all such views"""

        self.client.force_login(self.user)

        response_1 = self.client.get(self.url_1, {'amount':'20000','uuid':'Ref0954635898204'})
        self.assertEqual(response_1.status_code, 200)
        json_response_1 = json.loads(response_1.content)
        self.assertEqual(json_response_1['status'], True)
        self.assertEqual(json_response_1['message'], 'Transaction Created Successfully')

        response_2 = self.client.get(self.url_2, {'amount':'13000','uuid':'Ref0754825376493', 'recipient_email':'sarahabigaile@test.com'})
        self.assertEqual(response_2.status_code, 200)
        json_response_2 = json.loads(response_2.content)
        self.assertEqual(json_response_2['status'], True)
        self.assertEqual(json_response_2['message'], 'Transaction Created Successfully')

        response_3 = self.client.get(self.url_3, {'amount':'10000','uuid':'Ref0754365254894'})
        self.assertEqual(response_3.status_code, 200)
        json_response_3 = json.loads(response_3.content)
        self.assertEqual(json_response_3['status'], True)
        self.assertEqual(json_response_3['message'], 'Transaction Created Successfully')