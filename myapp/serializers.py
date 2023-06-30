from rest_framework import serializers
from myapp.models import AIwash


class myappSerializer(serializers.ModelSerializer):
    class Meta:
        model = AIwash
        fields = '__all__'