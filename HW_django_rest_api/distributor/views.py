from django.shortcuts import render
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import ProductSerializer, CategorySerializer, ProductCreateSerializer, ProductUpdateSerializer, \
    LoginValidateSerializer
from .models import Product, Category, Tag


# Create your views here.


@api_view(['GET', 'POST'])
def products_list_view(request):
    if request.method == 'GET':
        products = Product.objects.all()
        data = ProductSerializer(products, many=True).data
        return Response(data=data)
    elif request.method == 'POST':
        serializer = ProductCreateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                data={
                    'message': 'error',
                    'errors': serializer.errors
                }
            )
        product = Product.objects.create(
            title=request.data['title'],
            description=request.data['description'],
            price=request.data['price'],
            category_id=request.data['category_id']
        )
        for i in request.data['tags']:
            product.tags.add(i)
        product.save()
        return Response(data={'message': 'OK',
                              'product': ProductSerializer(product).data})


@api_view(['GET', 'PUT'])
def products_item_view(request, id):
    try:
        products = Product.objects.get(id=id)
    except Product.DoesNotExist:
        return Response(data={'message': 'Product does not exist!'}, status=status.HTTP_404_NOT_FOUND)
    if request.method == 'PUT':
        serializer = ProductUpdateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                data={
                    'message': 'error',
                    'errors': serializer.errors
                }
            )
        products.category_id = request.data['category_id']
        products.title = request.data['title']
        products.description = request.data['description']
        products.price = request.data['price']
        products.tags.clear()
        for i in request.data['tags']:
            products.tags.add(i)
        products.save()
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

from django.contrib import auth

@api_view(['POST'])
def login(request):
    if request.method == 'POST':
        serializer = LoginValidateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                data={
                    'message': 'error',
                    'errors':serializer.errors
                },
                status=status.HTTP_406_NOT_ACCEPTABLE
            )
        user = auth.authenticate(**serializer.validated_data)
        if user:
            try:
                token = Token.objects.get(user=user)
            except Token.DoesNotExist:
                token = Token.objects.create(user=user)
            return Response(data={'key': token.key})
        else:
            return Response(
                data={'message': 'Wrong login or password!'},
                status=status.HTTP_404_NOT_FOUND
            )