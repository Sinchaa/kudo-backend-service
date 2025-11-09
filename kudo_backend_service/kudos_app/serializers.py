from rest_framework import serializers
from .models import Kudo
from auth_app.models import User

class KudoSerializer(serializers.ModelSerializer):
    kudos_from = serializers.SerializerMethodField()
    kudos_to = serializers.SerializerMethodField()

    class Meta:
        model = Kudo
        fields = ['id', 'kudos_from', 'kudos_to', 'message', 'created_at', 'kudos_from', 'kudos_to']

    def get_kudos_from(self, obj):
        first = obj.kudos_from.first_name if obj.kudos_from.first_name else ''
        last = obj.kudos_from.last_name if obj.kudos_from.last_name else ''
        full_name = f"{first} {last}".strip()
        return full_name or obj.kudos_from.username  # Fallback to username

    def get_kudos_to(self, obj):
        first = obj.kudos_to.first_name if obj.kudos_to.first_name else ''
        last = obj.kudos_to.last_name if obj.kudos_to.last_name else ''
        full_name = f"{first} {last}".strip()
        return full_name or obj.kudos_to.username  # Fallback to username
    
class UserSerializer(serializers.ModelSerializer):
    organization = serializers.SerializerMethodField()
    class Meta:
        model= User
        fields = ['id', 'username', 'organization']
    
    def get_organization(self, obj):
        # return organization name (or id) — change as needed
        org = getattr(obj, 'organization', None)
        return org.name if org else None
