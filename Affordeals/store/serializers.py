from .models import Category, SiteUser, Products
from rest_framework import serializers


class SiteUserSerializer(serializers.ModelSerializer):
  user_id = serializers.IntegerField()
  class Meta:
    model = SiteUser
    fields = ['id', 'user_id', 'birth_date', 'phone_number']

class ProductsSerializer(serializers.ModelSerializer):
  class Meta:
    model = Products
    fields = ['id', 'name', 'unit_price']

class CategorySerializer(serializers.ModelSerializer):
  class Meta:
    model = Category
    fields = ['id', 'name']


