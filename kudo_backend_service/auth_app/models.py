from django.db import models
from django.contrib.auth.hashers import make_password, check_password
# Create your models here.
class User(models.Model):
    class Meta:
        db_table = 'user_tbl'
    username = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=128)  # Store hashed or plaintext as per your requirements
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    email = models.EmailField(blank=True)
    organization = models.ForeignKey('kudos_app.Organization', on_delete=models.CASCADE, related_name='users')
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)
    
    def _str_(self):
        return f'User info for {self.username}, ID: {self.id}, Organization ID: {self.organization.id}, Name: {self.first_name} {self.last_name}, Email: {self.email}, Password:{self.password}'
