from .models import Category, SiteUser, Products, ShoppingOrder,\
                    ShoppingOrderItem, ShoppingCart, ShoppingCartItem, Review
from rest_framework import serializers
from main.serializers import UserSerializer


class SiteUserSerializer(serializers.ModelSerializer):
  user_id = serializers.IntegerField()
  user = UserSerializer()
  class Meta:
    model = SiteUser
    fields = ['id', 'user_id', 'user', 'birth_date', 'phone_number']

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
  total_price = serializers.SerializerMethodField()
  class Meta:
    model = ShoppingOrderItem
    fields = ['id', 'products', 'unit_price', 'quantity', 'total_price']

  def get_total_price(self, order_items: ShoppingOrderItem):
    return order_items.products.unit_price * order_items.quantity
  

class ShoppingOrderSerializer(serializers.ModelSerializer):
  items = ShoppingOrderItemSerializer(many=True, read_only=True)
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
  
  def save(self, *args, **kwargs):
    quantity = self.validated_data['quantity']
    cart_id = self.context['cart_id']
    product_id = self.validated_data['products_id']

    try:
      new_item = ShoppingCartItem.objects.get(cart_id=cart_id, product_id=products_id)
      new_item.quantity += quantity # If you add the same product, it adds to the previous one
      new_item.save()
      self.instance = new_item
    except ShoppingCartItem.DoesNotExist:
      self.instance = ShoppingCartItem.objects.create(cart_id=cart_id, **self.validated_data)
      return self.instance
  products = CustomProductSerializer()

  class Meta:
    model = ShoppingCartItem
    fields = ['id', 'products', 'quantity']
  


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

# class NewOrderSerializer(serializers.Serializer):
#   shoppingcart_id = serializers.UUIDField()

#   def save(elf, **kwargs):
#     print(self.validated_data['shoppingcart_id'])
#     print(self.context['user_id']) 

class NewOrderSerializer(serializers.Serializer):
  cart_id = serializers.UUIDField()

  def save(self, **kwargs):
    user = self.context['request'].user.id
    (customer, created) = SiteUser.objects.get_or_create(user_id=user)
    print("1. The current user > customer: " + customer)
    my_order = ShoppingOrder.objects.create(siteuser=customer)
    print("2. Demo my order: ")
    print(my_order)
    cartitems = ShoppingCartItem.objects.\
                            select_related('products'). \
                            filter(cart_id=self.validated_data['cart_id'])
    print("3. The Cart items: ")
    print(cartitems)
    # order_list_items = [
    #                     ShoppingOrderItem(
    #                       order=my_order,
    #                       product = item.products,
    #                       unit_price=item.products.unit_price,
    #                       quantity=item.quantity
    #                     )for item in cartitems]
    # print("4. The list of order items: ")
    # print(order_list_items)
    order_list_items = []
    index = 0
    while index < len(cartitems):
      item = cartitems[index]
      order_list_items.append(
        ShoppingOrderItem(
            order=my_order,
            product=item.products,
            unit_price=item.products.unit_price,
            quantity=item.quantity
        )
      )
      index += 1
    ShoppingOrderItem.objects.bulk_create(order_list_items)
