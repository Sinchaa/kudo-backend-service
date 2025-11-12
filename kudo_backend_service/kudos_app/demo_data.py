import random
from django.utils import timezone
from .models import Organization, User, Kudo

def create_demo_data():
    # Create organizations
    org_names = ['Alpha Corp', 'Beta LLC', 'Gamma Inc']
    orgs = [Organization.objects.create(name=name) for name in org_names]

    # Create users
    users = []
    for i in range(10):
        org = random.choice(orgs)
        user = User.objects.create(
            username=f'user{i}',
            password='password',  # For demo only
            first_name=f'First{i}',
            last_name=f'Last{i}',
            email=f'user{i}@example.com',
            organization=org,
        )
        users.append(user)

    # Create kudos
    messages = [
        "Great job on the project!",
        "Thanks for your help!",
        "Awesome teamwork!",
        "Really appreciate your effort.",
        "You went above and beyond!",
    ]
    for _ in range(20):
        kudos_from, kudos_to = random.sample(users, 2)
        message = random.choice(messages)
        days_ago = random.randint(0, 14)
        created_at = timezone.now() - timezone.timedelta(days=days_ago)
        Kudo.objects.create(
            kudos_from=kudos_from,
            kudos_to=kudos_to,
            message=message,
            created_at=created_at
        )