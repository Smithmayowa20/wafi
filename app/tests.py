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
    - Test create user and profile model object creation
    - Test all transaction types model object creation
	- Test all transaction types views
    - Test check_balance view
	- Test login_required view decorator
    """

    @classmethod
    def setUpTestData(cls):
        cls.client = Client()
        cls.add_money = reverse('add_money')
        cls.send_money = reverse('send_money')
        cls.withdraw_money = reverse('withdraw_money')
        cls.check_balance = reverse('check_balance')

        cls.user = USER_MODEL.objects.create_user(
            email='johndoe@test.com',
            first_name='John',
            last_name='Doe',
            password='password456'
        )
        cls.profile = Profile.objects.create(
            first_name='John',
            last_name='Doe',
            user=cls.user,
            balance='50000',
		)


    def test_create_add_transaction(self):
        """ Tests that an add transaction object has been created with this uuid, amount and transaction type"""

        add_transaction_type = Transaction.objects.create(
            recipient=cls.user,
            amount='5000',
            transaction_uuid='Ref472749204',
            transaction_type='ADD',
        )
        self.assertEqual(add_transaction_type.amount, '5000')
        self.assertEqual(add_transaction_type.transaction_uuid, 'Ref472749204')
        self.assertEqual(add_transaction_type.transaction_type, 'ADD')
        self.assertEqual(add_transaction_type.recipient, self.user)

    def test_create_send_transaction(self):
        """ Tests that a send transaction object has been created with this uuid, amount and transaction type"""

        send_transaction_type = Transaction.objects.create(
            recipient=cls.user,
            amount='6000',
            transaction_uuid='Ref678749204',
            transaction_type='SEN',
        )

        self.assertEqual(send_transaction_type.amount, '6000')
        self.assertEqual(send_transaction_type.transaction_uuid, 'Ref678749204')
        self.assertEqual(send_transaction_type.transaction_type, 'SEN')
        self.assertEqual(send_transaction_type.recipient, self.user)

    def test_create_wth_transaction(self):
        """ Tests that a withdraw transaction object has been created with this uuid, amount and transaction type"""

        wth_transaction_type = Transaction.objects.create(
            recipient=cls.user,
            amount='7000',
            transaction_uuid='Ref0977749204',
            transaction_type='WTH',
        )

        self.assertEqual(wth_transaction_type.amount, '7000')
        self.assertEqual(wth_transaction_type.transaction_uuid, 'Ref0977749204')
        self.assertEqual(wth_transaction_type.transaction_type, 'WTH')
        self.assertEqual(wth_transaction_type.recipient, self.user)

    
    def test_user_must_be_logged_in(self):
        """ Tests that a non-logged in user is redirected """

        response_1 = self.client.get(self.url_1)
        self.assertEqual(response_1.status_code, 302)

        response_2 = self.client.get(self.url_2)
        self.assertEqual(response_2.status_code, 302)

        response_3 = self.client.get(self.url_3)
        self.assertEqual(response_3.status_code, 302)


class TestProfileCreationView(TestCase):
    """
    Things to test:
    - Test create profile model view
	"""

    @classmethod
    def setUpTestData(cls):
        cls.client = Client()
        cls.create_profile = reverse('create_profile')

        cls.user = USER_MODEL.objects.create_user(
            email='johndoe@test.com',
            first_name='John',
            last_name='Doe',
            password='password45678'
        )


    def test_create_profile_dollar_view(self):
        """ Tests create profile view with logged in user who has a USD default currency field"""

        self.client.force_login(self.user)

        response = self.client.get(self.create_profile, {
            'first_name'='Jake',
            'last_name'='Paul',
            'balance'='46000',
            'default_currency'='USD',
		})
        self.assertEqual(response.status_code, 200)
        json_response_1 = json.loads(response_1.content)
        self.assertEqual(json_response_1['status'], True)
        self.assertEqual(json_response_1['message'], 'User Profile Created Successfully')
        self.assertEqual(json_response_1['first_name'], 'Jake')
        self.assertEqual(json_response_1['balance'], '46000')
        self.assertEqual(json_response_1['default_currency'], 'USD')

    def test_create_profile_yen_view(self):
        """ Test create profile view with logged in user who has a YEN default currency field"""

        self.client.force_login(self.user)

        response = self.client.get(self.create_profile, {
            'first_name'='Fred',
            'last_name'='Sunny',
            'balance'='38000',
            'default_currency'='YEN',
		})
        self.assertEqual(response_1.status_code, 200)
        json_response_1 = json.loads(response_1.content)
        self.assertEqual(json_response_1['status'], True)
        self.assertEqual(json_response_1['message'], 'User Profile Created Successfully')
        self.assertEqual(json_response_1['first_name'], 'Fred')
        self.assertEqual(json_response_1['balance'], '38000')
        self.assertEqual(json_response_1['default_currency'], 'YEN')



class TestTransactionViews(TestCase):
    """
    Things to test:
	- Test all transaction type views
    """

    @classmethod
    def setUpTestData(cls):
        cls.client = Client()
        cls.add_money = reverse('add_money')
        cls.send_money = reverse('send_money')
        cls.withdraw_money = reverse('withdraw_money')

        cls.user_1 = USER_MODEL.objects.create_user(
            email='johndoe@test.com',
            first_name='John',
            last_name='Doe',
            password='password456'
        )
        cls.user_1_profile = Profile.objects.create(
            first_name='John',
            last_name='Doe',
            user=cls.user,
            balance='10000',
            default_currency='USD',
		)

        cls.user_2 = USER_MODEL.objects.create_user(
            email='sarahabigaile@test.com',
            first_name='Sarah',
            last_name='Abigail',
            password='password123'
        )
        cls.user_2_profile = Profile.objects.create(
            first_name='Sarah',
            last_name='Abigail',
            user=cls.user_2,
            balance='70000',
            default_currency='YEN',
		)


    def test_add_money_transaction_view(self):
        """ Tests add_money transaction view with a logged in user"""

        self.client.force_login(self.user_1)

        response_1 = self.client.get(self.add_money, {'amount':'20000','currency':'USD','uuid':'Ref0954635898204'})
        self.assertEqual(response_1.status_code, 200)
        json_response_1 = json.loads(response_1.content)
        self.assertEqual(json_response_1['status'], True)
        self.assertEqual(json_response_1['message'], 'Transaction Created Successfully')

    def test_send_money_transaction_view(self):
        """ Tests send_money transaction view with logged in user_1 to logged in user_2 and from USD to YEN"""

        self.client.force_login(self.user_1)

        response_2 = self.client.get(self.send_money, {'amount':'13000','currency':'USD','uuid':'Ref0754825376493', 'recipient_email':'sarahabigaile@test.com'})
        self.assertEqual(response_2.status_code, 200)
        json_response_2 = json.loads(response_2.content)
        self.assertEqual(json_response_2['status'], True)
        self.assertEqual(json_response_2['message'], 'Transaction Created Successfully')

    def test_withdraw_money_transaction_view(self):
        """ Tests withdraw_money transaction view in USD with logged in user_2 who has a default_currency in YEN"""

        self.client.force_login(self.user_2)

        response_3 = self.client.get(self.withdraw_money, {'amount':'10000','currency':'USD','uuid':'Ref0754365254894'})
        self.assertEqual(response_3.status_code, 200)
        json_response_3 = json.loads(response_3.content)
        self.assertEqual(json_response_3['status'], True)
        self.assertEqual(json_response_3['message'], 'Transaction Created Successfully')