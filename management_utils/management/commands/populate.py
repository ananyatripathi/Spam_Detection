from django.core.management.base import BaseCommand
from django.utils.crypto import get_random_string
from faker import Faker
from accounts.models import User
from contacts.models import Contact
from spam_management.models import Spam
import random

class Command(BaseCommand):
    help = 'Populates the database with sample data for testing.'

    def handle(self, *args, **kwargs):
        fake = Faker()
        phone_numbers = set()

        # Function to generate unique phone numbers
        def generate_unique_phone_number():
            phone_number = fake.phone_number()
            while phone_number in phone_numbers:
                phone_number = fake.phone_number()
            phone_numbers.add(phone_number)
            return phone_number

        # Create 50 users
        users = []
        for _ in range(50):
            phone_number = generate_unique_phone_number()
            user = User.objects.create_user(
                phone_number=phone_number,
                name=f'User {_}',
                password='securepassword'
            )
            users.append(user)

        # Create contacts for each user
        for user in users:
            for _ in range(random.randint(5, 10)):
                phone_number = generate_unique_phone_number()
                Contact.objects.create(
                    user=user,
                    phone_number=phone_number,
                    name=f'Contact {random.randint(1, 100)}'
                )

        # Add spam records
        # 10 users' phone numbers to spam
        spam_users = random.sample(users, 10)
        for user in spam_users:
            Spam.objects.create(
                phone_number=user.phone_number,
                spam_count=1,
                user=user
            )

        # 20 contacts' phone numbers to spam
        contacts = list(Contact.objects.all())
        spam_contacts = random.sample(contacts, 20)
        for contact in spam_contacts:
            Spam.objects.create(
                phone_number=contact.phone_number,
                spam_count=1,
                user=None  # If there's no associated user
            )

        # 10 random phone numbers in spam table
        for _ in range(10):
            phone_number = generate_unique_phone_number()
            Spam.objects.create(
                phone_number=phone_number,
                spam_count=1,
                user=None
            )

        # 5 numbers present in all three tables
        common_numbers = [generate_unique_phone_number() for _ in range(5)]
        for number in common_numbers:
            user = User.objects.create_user(
                phone_number=number,
                name=f'User {number}',
                password='securepassword'
            )
            Contact.objects.create(
                user=user,
                phone_number=number,
                name=f'Contact {number}'
            )
            Spam.objects.create(
                phone_number=number,
                spam_count=1,
                user=user
            )

        self.stdout.write(self.style.SUCCESS('Database populated with sample data.'))
