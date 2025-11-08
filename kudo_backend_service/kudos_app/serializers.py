from rest_framework import serializers
from .models import Kudo

class KudoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Kudo
        fields = '__all__'