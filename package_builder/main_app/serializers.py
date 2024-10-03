from rest_framework import serializers
from .models import Package, Build

class PackageSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Package
        fields = '__all__'
        read_only_fields = ['created_at']

class BuildSerializer(serializers.ModelSerializer):
    class Meta:
        model = Build
        fields = '__all__'
        read_only_fields = ['status', 'log', 'created_at']
