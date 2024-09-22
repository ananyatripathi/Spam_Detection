from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from accounts.models import User
from contacts.models import Contact
from spam_management.models import Spam
from .serializers import UserSerializer, ContactSerializer, SpamSerializer

class SearchView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        query = request.GET.get('q', '').strip()
        search_type = request.GET.get('type', 'name')
        seen_phone_numbers = set()
        results = []

        if search_type == 'name':
            # Searching for users by name
            users = User.objects.filter(
                Q(name__icontains=query)
            ).order_by('name')

            for user in users:
                spam_count = self.get_spam_count(user.phone_number)
                results.append({
                    'name': user.name,
                    'phone_number': user.phone_number,
                    'email': user.email,
                    'spam_count': spam_count
                })
                seen_phone_numbers.add(user.phone_number)

            # Searching for contacts by name
            contacts = Contact.objects.filter(
                Q(name__icontains=query)
            ).order_by('name')

            for contact in contacts:
                if contact.phone_number not in seen_phone_numbers:
                    spam_count = self.get_spam_count(contact.phone_number)
                    results.append({
                        'name': contact.name,
                        'phone_number': contact.phone_number,
                        'spam_count': spam_count
                    })
                    seen_phone_numbers.add(contact.phone_number)

        elif search_type == 'phone':
            # Searching for users by phone number (partial match)
            users = User.objects.filter(phone_number__icontains=query)
            for user in users:
                spam_count = self.get_spam_count(user.phone_number)
                results.append({
                    'name': user.name,
                    'phone_number': user.phone_number,
                    'email': user.email,
                    'spam_count': spam_count
                })
                seen_phone_numbers.add(user.phone_number)

            # Searching for contacts by phone number (partial match)
            contacts = Contact.objects.filter(phone_number__icontains=query)
            for contact in contacts:
                if contact.phone_number not in seen_phone_numbers:
                    spam_count = self.get_spam_count(contact.phone_number)
                    results.append({
                        'name': contact.name,
                        'phone_number': contact.phone_number,
                        'spam_count': spam_count
                    })
                    seen_phone_numbers.add(contact.phone_number)

            # Searching spam records by phone number (partial match)
            spam_records = Spam.objects.filter(phone_number__icontains=query)
            for spam in spam_records:
                if spam.phone_number not in seen_phone_numbers:
                    results.append({
                        'phone_number': spam.phone_number,
                        'spam_count': spam.spam_count
                    })
                    seen_phone_numbers.add(spam.phone_number)

        return Response(results)

    def get_spam_count(self, phone_number):
        """Helper method to get spam count for a phone number."""
        try:
            return Spam.objects.get(phone_number=phone_number).spam_count
        except Spam.DoesNotExist:
            return 0
