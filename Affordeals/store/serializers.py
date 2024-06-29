from .models import Category, SiteUser, Products, ShoppingOrder,\
                    ShoppingOrderItem, ShoppingCart, ShoppingCartItem
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

class CustomProductSerializer(serializers.ModelSerializer):
  class Meta:
    model = Products
    fields = ['id', 'name', 'unit_price']

class ShoppingOrderItemSerializer(serializers.ModelSerializer):
  products = CustomProductSerializer()
  class Meta:
    model = ShoppingOrderItem
    fields = ['id', 'products', 'unit_price', 'quantity']
  
   
class ShoppingOrderSerializer(serializers.ModelSerializer):
  items = ShoppingOrderItemSerializer(many=True)
  class Meta:
    model = ShoppingOrder
    fields = ['id', 'created_at', 'siteuser', 'payment_status', items]
