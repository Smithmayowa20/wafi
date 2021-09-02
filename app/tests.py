from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse

from app.models import Profile, Transaction

import json

# Create your tests here.
USER_MODEL = get_user_model()




class TestProfileCreationView(TestCase):
    """
    Things to test:
    - Test create profile view
    - Test login_required decorator
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

    
    def test_user_must_be_logged_in(self):
        """ Tests that a non-logged in user is redirected """

        response = self.client.get(self.create_profile)
        self.assertEqual(response.status_code, 302)

    def test_create_profile_dollar_view(self):
        """ Tests create profile view with logged in user who has a USD default currency field"""

        self.client.force_login(self.user)

        response = self.client.post(self.create_profile, {
            'first_name':'Jake',
            'last_name':'Paul',
            'balance':'46000.0',
            'default_currency':'USD',
		})
        self.assertEqual(response.status_code, 200)
        json_response = json.loads(response.content)
        self.assertEqual(json_response['status'], True)
        self.assertEqual(json_response['message'], 'User Profile Created Successfully')
        self.assertEqual(json_response['first_name'], 'Jake')
        self.assertEqual(json_response['balance'], '46000.0')
        self.assertEqual(json_response['default_currency'], 'USD')

    def test_create_profile_yen_view(self):
        """ Test create profile view with logged in user who has a YEN default currency field"""

        self.client.force_login(self.user)

        response = self.client.post(self.create_profile, {
            'first_name':'Fred',
            'last_name':'Sunny',
            'balance':'38000.0',
            'default_currency':'YEN',
		})
        self.assertEqual(response.status_code, 200)
        json_response = json.loads(response.content)
        self.assertEqual(json_response['status'], True)
        self.assertEqual(json_response['message'], 'User Profile Created Successfully')
        self.assertEqual(json_response['first_name'], 'Fred')
        self.assertEqual(json_response['balance'], '38000.0')
        self.assertEqual(json_response['default_currency'], 'YEN')




class TestCheckBalanceView(TestCase):
    """
    Things to test:
    - Test check_balance view
	"""

    @classmethod
    def setUpTestData(cls):
        cls.client = Client()
        cls.check_balance = reverse('check_balance')

        cls.user = USER_MODEL.objects.create_user(
            email='johndoe@test.com',
            first_name='John',
            last_name='Doe',
            password='password45678'
        )
        cls.profile = Profile.objects.create(
            first_name='Lucas',
            last_name='Kola',
            user=cls.user,
            balance='2300500.0',
            default_currency='NGN',
		)

    def test_check_balance_view(self):
        """ Tests a user's profile balance lookup"""

        self.client.force_login(self.user)

        response = self.client.get(self.check_balance, {})
        self.assertEqual(response.status_code, 200)
        json_response = json.loads(response.content)
        self.assertEqual(json_response['balance'], '2300500.0')
        self.assertEqual(json_response['default_currency'], 'NGN')
        self.assertEqual(json_response['status'], True)
        self.assertEqual(json_response['message'], 'User Balance Checked Successfully')




class TestTransactionModelTypesCreation(TestCase):
    """
    Things to test:
    - Test all transaction types model object creation
    """

    @classmethod
    def setUpTestData(cls):
        cls.client = Client()

        cls.user_1 = USER_MODEL.objects.create_user(
            email='johndoe@test.com',
            first_name='John',
            last_name='Doe',
            password='password456'
        )
        cls.user_1_profile = Profile.objects.create(
            first_name='John',
            last_name='Doe',
            user=cls.user_1,
            balance='10000.0',
            default_currency='USD',
		)

        cls.user_2 = USER_MODEL.objects.create_user(
            email='janedoe@test.com',
            first_name='Jane',
            last_name='Doe',
            password='password430'
        )
        cls.user_2_profile = Profile.objects.create(
            first_name='Jane',
            last_name='Doe',
            user=cls.user_2,
            balance='70000.0',
            default_currency='YEN',
		)


    def test_create_add_transaction(self):
        """ Tests that an add transaction object has been created with this uuid, currency_type, amount and transaction type"""

        add_transaction_type = Transaction.objects.create(
            recipient=self.user_1,
            amount='5000.0',
            transaction_uuid='Ref472749204',
            transaction_type='ADD',
            currency_type='USD',
        )
        self.assertEqual(add_transaction_type.amount, '5000.0')
        self.assertEqual(add_transaction_type.transaction_uuid, 'Ref472749204')
        self.assertEqual(add_transaction_type.transaction_type, 'ADD')
        self.assertEqual(add_transaction_type.currency_type, 'USD')
        self.assertEqual(add_transaction_type.recipient, self.user_1)

    def test_create_send_transaction(self):
        """ Tests that a send transaction object has been created with this uuid, currency_type, amount and transaction type"""

        send_transaction_type = Transaction.objects.create(
            sender=self.user_1,
            recipient=self.user_2,
            amount='6000.0',
            transaction_uuid='Ref678749204',
            transaction_type='SEN',
            currency_type='YEN',
        )

        self.assertEqual(send_transaction_type.amount, '6000.0')
        self.assertEqual(send_transaction_type.transaction_uuid, 'Ref678749204')
        self.assertEqual(send_transaction_type.transaction_type, 'SEN')
        self.assertEqual(send_transaction_type.currency_type, 'YEN')
        self.assertEqual(send_transaction_type.sender, self.user_1)
        self.assertEqual(send_transaction_type.recipient, self.user_2)

    def test_create_wth_transaction(self):
        """ Tests that a withdraw transaction object has been created with this uuid, currency_type, amount and transaction type"""

        wth_transaction_type = Transaction.objects.create(
            sender=self.user_1,
            amount='7000.0',
            transaction_uuid='Ref0977749204',
            transaction_type='WTH',
            currency_type='NGN',
        )

        self.assertEqual(wth_transaction_type.amount, '7000.0')
        self.assertEqual(wth_transaction_type.transaction_uuid, 'Ref0977749204')
        self.assertEqual(wth_transaction_type.transaction_type, 'WTH')
        self.assertEqual(wth_transaction_type.currency_type, 'NGN')
        self.assertEqual(wth_transaction_type.sender, self.user_1)





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
            user=cls.user_1,
            balance='100000.0',
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
            balance='7000000.0',
            default_currency='YEN',
		)


    def test_add_money_transaction_view(self):
        """ Tests add_money transaction view with a logged in user"""

        self.client.force_login(self.user_1)

        response = self.client.get(self.add_money, {'amount':'20000.0','currency':'USD','uuid':'Ref0954635898204'})
        self.assertEqual(response.status_code, 200)
        json_response = json.loads(response.content)
        self.assertEqual(json_response['recipient_balance'], '120000.0')
        self.assertEqual(json_response['status'], True)
        self.assertEqual(json_response['message'], 'Transaction Created Successfully')

    def test_send_money_transaction_view(self):
        """ Tests send_money transaction view with logged in user_1 to logged in user_2 and from USD to YEN"""

        self.client.force_login(self.user_1)

        response = self.client.get(self.send_money, {'amount':'13000.0','currency':'USD','uuid':'Ref0754825376493', 'recipient_email':'sarahabigaile@test.com'})
        self.assertEqual(response.status_code, 200)
        json_response = json.loads(response.content)
        self.assertEqual(json_response['recipient_balance'], '8423110.0')
        self.assertEqual(json_response['sender_balance'], '87000.0')
        self.assertEqual(json_response['status'], True)
        self.assertEqual(json_response['message'], 'Transaction Created Successfully')

    def test_withdraw_money_transaction_view(self):
        """ Tests withdraw_money transaction view in USD with logged in user_2 who has a default_currency in YEN"""

        self.client.force_login(self.user_2)

        response = self.client.get(self.withdraw_money, {'amount':'10000.0','currency':'USD','uuid':'Ref0754365254894'})
        self.assertEqual(response.status_code, 200)
        json_response = json.loads(response.content)
        self.assertEqual(json_response['sender_balance'], '5905300.0')
        self.assertEqual(json_response['status'], True)
        self.assertEqual(json_response['message'], 'Transaction Created Successfully')