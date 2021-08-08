from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import Category, Tag, Product


class ProductSerializer(serializers.ModelSerializer):
    tags = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = 'title description price category tags'.split()

    def get_tags(self, brand):
        l = []
        for i in brand.tags.all():
            l.append(i.name)
        return l


class CategorySerializer(serializers.ModelSerializer):
    category_pr = ProductSerializer(many=True)

    class Meta:
        model = Category
        fields = 'id name category_pr'.split()


class ProductCreateSerializer(serializers.Serializer):
    title = serializers.CharField(min_length=2, max_length=100)
    description = serializers.CharField(max_length=100)
    price = serializers.IntegerField()
    category_id = serializers.IntegerField()
    tags = serializers.ListField(required=False, child=serializers.IntegerField())

    def validate_title(self, title):
        products = Product.objects.filter(title=title)
        if products.count() > 0:
            raise ValidationError('Такой товар уже существует!')

    def validate_tags(self, tags):
        if Tag.objects.filter(id__in=tags).count() != len(tags):
            raise ValidationError('Tags error')

    def validate(self, attrs):
        id = attrs['category_id']
        if Category.objects.filter(id=id) is not None:
            raise ValidationError('Такой категории не существует')
        return attrs


class ProductUpdateSerializer(serializers.Serializer):
    title = serializers.CharField(min_length=2, max_length=100)
    description = serializers.CharField(max_length=100)
    price = serializers.IntegerField()
    category_id = serializers.IntegerField()
    tags = serializers.ListField(required=False, child=serializers.IntegerField())

    def validate_tags(self, tags):
        if Tag.objects.filter(id__in=tags).count() != len(tags):
            raise ValidationError('Tags error')

    def validate(self, attrs):
        id = attrs['category_id']
        if Category.objects.filter(id=id) is not None:
            raise ValidationError('Такой категории не существует')
        return attrs
