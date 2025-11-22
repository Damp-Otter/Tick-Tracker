from rest_framework import serializers
from .models import TickModel

class TickSerializer(serializers.ModelSerializer):
    class Meta:
        model = TickModel
        fields = '__all__'