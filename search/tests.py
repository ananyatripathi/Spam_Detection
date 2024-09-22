from django.test import TestCase, Client
from rest_framework import status
from django.contrib.auth import get_user_model
from contacts.models import Contact
from spam_management.models import Spam
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()

class SearchViewTestCase(TestCase):
    def setUp(self):
        # Create test users
        self.user1 = User.objects.create_user(phone_number='1234567890', name='Alice', password='password123')
        self.user2 = User.objects.create_user(phone_number='0987654321', name='Bob', password='password123')
        self.user3 = User.objects.create_user(phone_number='5555555555', name='Charlie', password='password123')

        # Create test contacts
        Contact.objects.create(user=self.user1, phone_number='1111111111', name='Alice Contact')
        Contact.objects.create(user=self.user2, phone_number='2222222222', name='Bob Contact')

        # Create test spam records
        Spam.objects.create(phone_number='1111111111', spam_count=3, user=self.user1)
        Spam.objects.create(phone_number='2222222222', spam_count=5, user=self.user2)
        Spam.objects.create(phone_number='3333333333', spam_count=2, user=self.user3)

        # Obtain JWT token for authentication
        refresh = RefreshToken.for_user(self.user1)
        self.token = str(refresh.access_token)
        
        # Initialize the test client
        self.client = Client()
        self.client.defaults['HTTP_AUTHORIZATION'] = f'Bearer {self.token}'

    def test_search_by_name_found_in_contact(self):
        response = self.client.get('/api/search/', {'q': 'Bob Contact', 'type': 'name'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'Bob Contact')
        self.assertEqual(response.data[0]['phone_number'], '2222222222')
        self.assertEqual(response.data[0]['spam_count'], 5)

    def test_search_by_phone_number_found_in_contact(self):
        response = self.client.get('/api/search/', {'q': '1111', 'type': 'phone'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'Alice Contact')
        self.assertEqual(response.data[0]['phone_number'], '1111111111')
        self.assertEqual(response.data[0]['spam_count'], 3)

    def test_search_by_phone_number_found_in_spam(self):
        response = self.client.get('/api/search/', {'q': '3333', 'type': 'phone'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['phone_number'], '3333333333')
        self.assertEqual(response.data[0]['spam_count'], 2)

    def test_search_by_name_no_results(self):
        response = self.client.get('/api/search/', {'q': 'Nonexistent', 'type': 'name'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [])

    def test_search_by_phone_number_no_results(self):
        response = self.client.get('/api/search/', {'q': '9999', 'type': 'phone'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [])

    def test_search_by_name_with_duplicate_numbers(self):
        Contact.objects.create(user=self.user1, phone_number='5555555555', name='Duplicate Contact')
        response = self.client.get('/api/search/', {'q': 'Duplicate Contact', 'type': 'name'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['phone_number'], '5555555555')

    def test_search_by_phone_number_with_duplicate_numbers(self):
        Contact.objects.create(user=self.user1, phone_number='5555555555', name='Duplicate Contact')
        response = self.client.get('/api/search/', {'q': '555', 'type': 'phone'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['phone_number'], '5555555555')
