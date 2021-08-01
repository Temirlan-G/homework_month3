from rest_framework import serializers
from .models import Category, Tag, Product


class TagsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = 'id name'.split()


class ProductSerializer(serializers.ModelSerializer):
    tags = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = 'title description price tags'.split()

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
