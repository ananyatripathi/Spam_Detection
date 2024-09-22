from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model

User = get_user_model()

class UserProfileTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            phone_number='1234567890', name='Test User', password='securepassword', email='test@example.com'
        )
        self.client.force_authenticate(user=self.user)

    def test_get_user_profile(self):
        response = self.client.get(reverse('user-profile'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Test User')
        self.assertEqual(response.data['email'], 'test@example.com')

    def test_update_user_profile(self):
        data = {'name': 'Updated User', 'email': 'updated@example.com'}
        response = self.client.put(reverse('user-profile'), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.name, 'Updated User')
        self.assertEqual(self.user.email, 'updated@example.com')
