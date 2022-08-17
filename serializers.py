from rest_framework import serializers
from .models import Product
from rest_framework.generic import ListAPIView

class ProductSerializers(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'