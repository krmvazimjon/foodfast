from rest_framework import serializers
from .models import User
from my_app.models import Product
from rest_framework.generics import ListAPIView

class ProductSerializers(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class UserSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

    def create(self, validated_data):
        auth_user = User.objects.create_user(**validated_data)
        return auth_user