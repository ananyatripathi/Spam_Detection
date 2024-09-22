from django.db import models
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Spam
from .serializers import SpamNumberSerializer

class MarkSpamView(generics.CreateAPIView):
    serializer_class = SpamNumberSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        phone_number = serializer.validated_data['phone_number']
        user = self.request.user

        # Check if the phone number is already marked as spam by this user
        existing_spam_record = Spam.objects.filter(phone_number=phone_number, user=user).first()

        if existing_spam_record:
            return Response({'message': 'This number is already marked as spam by you.'}, status=status.HTTP_400_BAD_REQUEST)

        # Create a new spam record
        serializer.save(user=user, spam_count=1)  # Initialize spam_count as 1

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone_number = serializer.validated_data['phone_number']

        # Check if the phone number already exists in the Spam table
        spam_record = Spam.objects.filter(phone_number=phone_number).first()

        if spam_record:
            # Increment the spam count if the record exists and the current user has already marked it
            if Spam.objects.filter(phone_number=phone_number, user=request.user).exists():
                return Response({'message': 'This number is already marked as spam by you.'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                # Increment the spam count if it exists but the current user has not marked it
                spam_record.spam_count += 1
                spam_record.save()
        else:
            # Create a new record with spam_count as 1
            self.perform_create(serializer)

        # Get the spam count for the phone number
        spam_count = Spam.objects.filter(phone_number=phone_number).aggregate(
            total_spam_count=models.Sum('spam_count')
        )['total_spam_count'] or 0

        return Response({'message': 'Phone number marked as spam.', 'spam_count': spam_count}, status=status.HTTP_201_CREATED)
