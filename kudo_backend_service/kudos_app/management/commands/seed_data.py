from django.core.management.base import BaseCommand
from django.contrib.auth.hashers import make_password
from kudos_app.models import Organization, Kudo
from auth_app.models import User

class Command(BaseCommand):
    help = "Seed sample organizations, users and kudos (idempotent)."

    def handle(self, *args, **options):
        org1, _ = Organization.objects.get_or_create(name="Alpha Org")
        org2, _ = Organization.objects.get_or_create(name="Beta Org")

        users = [
            ("alice", "pass", "Alice", "Anderson", "alice@example.com", org1),
            ("bob", "pass", "Bob", "Brown", "bob@example.com", org1),
            ("carol", "pass", "Carol", "Clark", "carol@example.com", org2),
            ("dave", "pass", "Dave", "Davis", "dave@example.com", org1),
            ("eve", "pass", "Eve", "Evans", "eve@example.com", org2),
            ("frank", "pass", "Frank", "Foster", "frank@example.com", org2),
            ("grace", "pass", "Grace", "Green", "grace@example.com", org1),
        ]

        for username, password, first, last, email, org in users:
            user, created = User.objects.get_or_create(
                username=username,
                defaults={
                    "password": make_password(password),
                    "first_name": first,
                    "last_name": last,
                    "email": email,
                    "organization": org,
                },
            )
            # Ensure password is hashed if user existed with plaintext
            if not user.password.startswith("pbkdf2_"):
                user.password = make_password(password)
                user.save()

        # create sample kudos (get_or_create makes this idempotent)
        def g(u_from, u_to, msg):
            Kudo.objects.get_or_create(
                kudos_from=User.objects.get(username=u_from),
                kudos_to=User.objects.get(username=u_to),
                message=msg,
            )

        g("alice", "bob", "Great teamwork!")
        g("bob", "alice", "Thanks for your help!")
        g("carol", "alice", "Well done on the project!")

        self.stdout.write(self.style.SUCCESS("Sample data seeded (or already present)."))