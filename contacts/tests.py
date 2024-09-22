from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from .models import Contact

User = get_user_model()

class ContactTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            phone_number='1234567890', name='Test User', password='securepassword', email='test@example.com'
        )
        self.client.force_authenticate(user=self.user)

    def test_add_contact(self):
        data = {'phone_number': '0987654321', 'name': 'Contact User'}
        response = self.client.post(reverse('contact-list'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Contact.objects.count(), 1)
        self.assertEqual(Contact.objects.get().name, 'Contact User')

    def test_get_contacts(self):
        Contact.objects.create(user=self.user, phone_number='0987654321', name='Contact User')
        response = self.client.get(reverse('contact-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_delete_contact(self):
        contact = Contact.objects.create(user=self.user, phone_number='0987654321', name='Contact User')
        response = self.client.delete(reverse('contact-detail', kwargs={'pk': contact.pk}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Contact.objects.count(), 0)
