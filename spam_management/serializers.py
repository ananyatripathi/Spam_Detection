# spam/serializers.py
from rest_framework import serializers
from .models import Spam

class SpamNumberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Spam
        fields = ['phone_number']
