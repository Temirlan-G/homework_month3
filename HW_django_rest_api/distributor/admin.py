from django.contrib import admin
from distributor.models import Category, Tag, Product

# Register your models here.

admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Product)
