from .models import Category, SiteUser, Products, ShoppingOrder, ShoppingCart, ShoppingCartItem, ShoppingOrderItem
from rest_framework import serializers


class SiteUserSerializer(serializers.ModelSerializer):
  """
    Serializer for SiteUser model.

    Fields:
    - id (int): The unique identifier of the site user.
    - user_id (int): The ID of the associated user.
    - birth_date (Date): The birth date of the site user.
    - phone_number (str): The phone number of the site user.
  """
  user_id = serializers.IntegerField()
  class Meta:
    model = SiteUser
    fields = ['id', 'user_id', 'birth_date', 'phone_number']

class ProductsSerializer(serializers.ModelSerializer):
  """
    Serializer for Products model.

    Fields:
    - id (int): The unique identifier of the product.
    - name (str): The name of the product.
    - unit_price (Decimal): The unit price of the product.
  """
  class Meta:
    model = Products
    fields = ['id', 'name', 'unit_price']

class CategorySerializer(serializers.ModelSerializer):
  """
    Serializer for Category model.

    Fields:
    - id (int): The unique identifier of the category.
    - name (str): The name of the category.
  """
  class Meta:
    model = Category
    fields = ['id', 'name']

class CustomProductSerializer(serializers.ModelSerializer):
  """
    Custom serializer for Products model with specific fields.

    Fields:
    - id (int): The unique identifier of the product.
    - name (str): The name of the product.
    - unit_price (Decimal): The unit price of the product.
  """
  class Meta:
    model = Products
    fields = ['id', 'name', 'unit_price']

class ShoppingOrderItemSerializer(serializers.ModelSerializer):
  """
    Serializer for ShoppingOrderItem model.

    Fields:
    - id (int): The unique identifier of the order item.
    - products (CustomProductSerializer): The product associated with the order item.
    - quantity (int): The quantity of the product in the order item.
  """
  products = CustomProductSerializer()
  class Meta:
    model = ShoppingOrderItem
    fields = ['id', 'products', 'unit_price', 'quantity']
  
   
class ShoppingOrderSerializer(serializers.ModelSerializer):
  """
    Serializer for ShoppingOrder model.

    Fields:
    - id (int): The unique identifier of the order.
    - created_at (DateTime): The timestamp when the order was created.
    - siteuser (SiteUser): The user who placed the order.
    - payment_status (str): The payment status of the order.
  """
  items = ShoppingOrderItemSerializer(many=True)
  class Meta:
    model = ShoppingOrder
    fields = ['id', 'created_at', 'siteuser', 'payment_status', 'items']
