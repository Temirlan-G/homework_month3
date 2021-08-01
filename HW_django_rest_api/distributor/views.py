from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import ProductSerializer, CategorySerializer
from .models import Product, Category, Tag


# Create your views here.


@api_view(['GET', 'POST'])
def products_list_view(request):
    products = Product.objects.all()
    data = ProductSerializer(products, many=True).data
    return Response(data=data)


@api_view(['GET'])
def products_item_view(request, id):
    products = Product.objects.get(id=id)
    data = ProductSerializer(products).data
    return Response(data=data)


@api_view(['GET'])
def category_list_view(request):
    category = Category.objects.all()
    data = CategorySerializer(category, many=True).data
    return Response(data=data)


@api_view(['GET'])
def category_item_view(request, id):
    category = Category.objects.get(id=id)
    data = CategorySerializer(category).data
    return Response(data=data)