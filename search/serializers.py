from rest_framework import serializers
from accounts.models import User
from contacts.models import Contact
from spam_management.models import Spam

class UserSerializer(serializers.ModelSerializer):
    spam_likelihood = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['name', 'phone_number', 'email', 'spam_likelihood']

    def get_spam_likelihood(self, obj):
        try:
            spam = Spam.objects.get(phone_number=obj.phone_number)
            return spam.spam_count
        except Spam.DoesNotExist:
            return 0

class ContactSerializer(serializers.ModelSerializer):
    spam_likelihood = serializers.SerializerMethodField()

    class Meta:
        model = Contact
        fields = ['name', 'phone_number', 'spam_likelihood']

    def get_spam_likelihood(self, obj):
        try:
            spam = Spam.objects.get(phone_number=obj.phone_number)
            return spam.spam_count
        except Spam.DoesNotExist:
            return 0

class SpamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Spam
        fields = ['phone_number', 'spam_count']
