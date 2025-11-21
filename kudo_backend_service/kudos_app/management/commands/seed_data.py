from django.core.management.base import BaseCommand
from kudos_app.models import Organization, Kudo
from auth_app.models import User
from django.contrib.auth.hashers import make_password

class Command(BaseCommand):
    help = 'Populate database with dummy data for testing'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing data before seeding',
        )

    def handle(self, *args, **kwargs):
        # Clear data if --clear flag is provided
        if kwargs['clear']:
            self.stdout.write('Clearing existing data...')
            Kudo.objects.all().delete()
            User.objects.all().delete()
            Organization.objects.all().delete()
            self.stdout.write(self.style.WARNING('Cleared all existing data'))

        self.stdout.write('Starting to populate database...')

        # Create organizations
        self.stdout.write('Creating organizations...')
        org1, created = Organization.objects.get_or_create(name="Alpha Org")
        if created:
            self.stdout.write(self.style.SUCCESS(f'Created organization: {org1.name}'))
        else:
            self.stdout.write(f'Organization already exists: {org1.name}')
        
        org2, created = Organization.objects.get_or_create(name="Beta Org")
        if created:
            self.stdout.write(self.style.SUCCESS(f'Created organization: {org2.name}'))
        else:
            self.stdout.write(f'Organization already exists: {org2.name}')

        # Create users
        self.stdout.write('Creating users...')
        users_data = [
            ("alice", "Alice", "Anderson", "alice@example.com", org1),
            ("bob", "Bob", "Brown", "bob@example.com", org1),
            ("carol", "Carol", "Clark", "carol@example.com", org2),
            ("dave", "Dave", "Davis", "dave@example.com", org1),
            ("eve", "Eve", "Evans", "eve@example.com", org2),
            ("frank", "Frank", "Foster", "frank@example.com", org2),
            ("grace", "Grace", "Green", "grace@example.com", org1),
        ]

        created_users = []
        for username, first, last, email, org in users_data:
            user, created = User.objects.get_or_create(
                username=username,
                defaults={
                    'password': make_password("pass"),
                    'first_name': first,
                    'last_name': last,
                    'email': email,
                    'organization': org,
                    'is_active': True
                }
            )
            created_users.append(user)
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created user: {username}'))
            else:
                self.stdout.write(f'User already exists: {username}')

        # Create kudos
        self.stdout.write('Creating kudos...')
        if len(created_users) >= 2:
            kudo, created = Kudo.objects.get_or_create(
                kudos_from=created_users[0],  # alice
                kudos_to=created_users[1],    # bob
                defaults={'message': "Great teamwork!"}
            )
            if created:
                self.stdout.write(self.style.SUCCESS('Created sample kudo'))
            else:
                self.stdout.write('Sample kudo already exists')

        self.stdout.write(self.style.SUCCESS('Successfully populated database with dummy data!'))