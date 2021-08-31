from app.models import Transaction
from django.test import TestCase
from django.contrib.auth import get_user_model

# Create your tests here.
USER_MODEL = get_user_model()


class TestTransactionModelAndView(TestCase):
    """
    Things to test:
    - Test all transaction types
	- Test login_required view decorator
    """

    @classmethod
    def setUpUserData(cls):
	    cls.client = Client()
        cls.url_1 = reverse('add_money')
        cls.url_2 = reverse('send_money')
        cls.url_3 = reverse('withdraw_money')

        cls.user = USER_MODEL.objects.create_user(
            email='janedoe@test.com',
            first_name='Jane',
            last_name='Doe',
            password='password456'
        )
        cls.profile = Profile.objects.create(
            first_name='Jane',
            last_name='Doe',
            user=cls.user,
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

    def test_create_profile(self):
        """ Tests that a profile object has been created with this first_name && user foreign field"""

        self.assertEqual(self.profile.first_name, 'John')
        self.assertEqual(self.profile.user, self.user)

    def test_create_add_transaction(self):
        """ Tests that an add transaction object has been created with this uuid, amount and transaction type"""

        self.assertEqual(self.add_transaction_type.amount, '5000')
        self.assertEqual(self.add_transaction_type.transaction_uuid, 'Ref472749204')
        self.assertEqual(self.add_transaction_type.transaction_type, 'ADD')
        self.assertEqual(self.transaction.recipient, self.user)

    def test_create_send_transaction(self):
        """ Tests that a send transaction object has been created with this uuid, amount and transaction type"""

        self.assertEqual(self.send_transaction_type.amount, '6000')
        self.assertEqual(self.send_transaction_type.transaction_uuid, 'Ref678749204')
        self.assertEqual(self.send_transaction_type.transaction_type, 'SEN')
        self.assertEqual(self.transaction.recipient, self.user)

    def test_create_wth_transaction(self):
        """ Tests that a withdraw transaction object has been created with this uuid, amount and transaction type"""

        self.assertEqual(self.wth_transaction_type.amount, '7000')
        self.assertEqual(self.wth_transaction_type.transaction_uuid, 'Ref0977749204')
        self.assertEqual(self.wth_transaction_type.transaction_type, 'WTH')
        self.assertEqual(self.transaction.recipient, self.user)

    
    def test_user_must_be_logged_in(self):
        """ Tests that a non-logged in user is redirected """

        response_1 = self.client.get(self.url_1)
        self.assertEqual(response_1.status_code, 302)

        response_2 = self.client.get(self.url_2)
        self.assertEqual(response_2.status_code, 302)

        response_3 = self.client.get(self.url_3)
        self.assertEqual(response_3.status_code, 302)

