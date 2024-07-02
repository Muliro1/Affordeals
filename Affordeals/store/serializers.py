<<<<<<< HEAD
from .models import Category, SiteUser, Products, ShoppingOrder, ShoppingCart, ShoppingCartItem, ShoppingOrderItem
=======
from django.db import transaction
from .models import Category, SiteUser, Products, ShoppingOrder,\
                    ShoppingOrderItem, ShoppingCart, ShoppingCartItem, Review
>>>>>>> main
from rest_framework import serializers
from main.serializers import UserSerializer


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
    fields = ['id', 'name', 'quantity_in_stock', 'unit_price']

class CategorySerializer(serializers.ModelSerializer):
  """
    Serializer for Category model.

    Fields:
    - id (int): The unique identifier of the category.
    - name (str): The name of the category.
  """
  product_count = serializers.IntegerField(read_only=True)
  class Meta:
    model = Category
    fields = ['id', 'name', 'product_count']

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
  total_price = serializers.SerializerMethodField()
  class Meta:
    model = ShoppingOrderItem
    fields = ['id', 'products', 'quantity', 'total_price']

  def get_total_price(self, order_items: ShoppingOrderItem):
    return order_items.products.unit_price * order_items.quantity
  

class ShoppingOrderSerializer(serializers.ModelSerializer):
  items = ShoppingOrderItemSerializer(many=True)
  total_price = serializers.SerializerMethodField()
  class Meta:
    model = ShoppingOrder
    fields = ['id', 'created_at', 'siteuser', 'items', 'payment_status', 'total_price']

  def get_total_price(self, order_items: ShoppingOrder):
    return sum([item.products.unit_price * item.quantity for item in order_items.items.all()])

class ReviewSerializer(serializers.ModelSerializer):
  class Meta:
    model = Review
    fields = ['id', 'name', 'description', 'date']

  def create(self, validated_data):
    products_id = self.context['products_id']
    return Review.objects.create(products_id=products_id, **validated_data)


class AddShoppingCartItemSerializer(serializers.ModelSerializer):
  product_id = serializers.IntegerField()

  def validate_products_id(self, new_id):
    if Products.objects.filter(pk=new_id) is None:
      raise serializers.ValidationError(
        f"This {products_id} is invalid id insertion.")
      return new_id
  
  def save(self, **kwargs):
    quantity = self.validated_data['quantity']
    cart_id = self.context['cart_id']
    product_id = self.validated_data['product_id']

    try:
      new_item = ShoppingCartItem.objects.get(cart_id=cart_id, product_id=product_id)
      new_item.quantity += quantity # If you add the same product, it adds to the previous one
      new_item.save()
      self.instance = new_item
    except ShoppingCartItem.DoesNotExist:
      self.instance = ShoppingCartItem.objects.create(cart_id=cart_id,
                                                      product_id=product_id,
                                                      quantity=quantity)
    return self.instance
  class Meta:
    model = ShoppingCartItem
    fields = ['id', 'product_id', 'quantity']
  


class ShoppingCartItemSerializer(serializers.ModelSerializer):
  total_price = serializers.SerializerMethodField()
  product = CustomProductSerializer()
  class Meta:
    model = ShoppingCartItem
    fields = ['id', 'product', 'quantity', 'total_price']
  
  def get_total_price(self, items: ShoppingCartItem):
    return items.product.unit_price * items.quantity

class ShoppingCartSerializer(serializers.ModelSerializer):
  id = serializers.UUIDField(read_only=True)
  cartitems = ShoppingCartItemSerializer(many=True, read_only=True)
  total_price = serializers.SerializerMethodField()
  class Meta:
    model = ShoppingCart
    fields = ['id', 'created_at', 'cartitems', 'total_price']
  
  def get_total_price(self, cart: ShoppingCart):
    return sum([item.product.unit_price * item.quantity for item in cart.cartitems.all()])

class UpdateShoppingCartItemSerializer(serializers.ModelSerializer):
  class Meta:
    model = ShoppingCartItem
    fields = ['quantity']


class NewOrderSerializer(serializers.Serializer):
  cart_id = serializers.UUIDField()

  def validate_cart_id(self, id):
    if ShoppingCart.objects.filter(pk=id) is None:
      raise serializers.ValidationError(
        f"This {id} is an invalid id."
      )
    if ShoppingCartItem.objects.filter(cart_id=id).count() == 0:
      raise serializers.ValidationError(
        f"{id}: is empty"
      )
    return id

  def save(self, **kwargs):
    with transaction.atomic():
      user_id = self.context['user_id']
      customer = SiteUser.objects.get(user_id=user_id)
      my_order = ShoppingOrder.objects.create(siteuser=customer)
      cart_id = self.validated_data['cart_id']
      cartitems = ShoppingCartItem.objects.\
                            select_related('product'). \
                            filter(cart_id=cart_id)
      order_list_items = []
      index = 0
      while index < len(cartitems):
        item = cartitems[index]
        order_list_items.append(
          ShoppingOrderItem(
            order=my_order,
            products=item.product,
            unit_price=item.product.unit_price,
            quantity=item.quantity
          )
        )
        index += 1 
      ShoppingOrderItem.objects.bulk_create(order_list_items)
      ShoppingCart.objects.filter(pk=cart_id).delete()
      return my_order

class UpdateShoppingOrderSerializer(serializers.ModelSerializer):
  class Meta:
    model = ShoppingOrder
    fields = ['payment_status']
