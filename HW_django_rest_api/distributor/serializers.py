from rest_framework import serializers
from .models import Category, Tag, Product

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
