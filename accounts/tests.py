from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import User

class UserRegistrationTests(APITestCase):
    def test_register_user(self):
        url = reverse('register')
        data = {
            'phone_number': '1234567890',
            'name': 'Test User',
            'password': 'testpassword'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().phone_number, '1234567890')
