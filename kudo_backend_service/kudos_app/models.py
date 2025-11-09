from django.db import models
from auth_app.models import User

class Organization(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Kudo(models.Model):
    kudos_from = models.ForeignKey(User, related_name='kudos_given', on_delete=models.CASCADE)
    kudos_to = models.ForeignKey(User, related_name='kudos_received', on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Kudo from {self.kudos_from} to {self.kudos_to} at {self.created_at}'