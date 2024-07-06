from django.shortcuts import get_object_or_404, render
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser, DjangoModelPermissions
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, DestroyModelMixin
from .serializers import SiteUserSerializer
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from .models import SiteUser, Products, Category, ShoppingOrder, ShoppingOrderItem, Review, ShoppingCart, ShoppingCartItem, ShoppingCart
from .serializers import SiteUserSerializer, ProductsSerializer, CategorySerializer,\
                         ShoppingOrderSerializer, ShoppingOrderItemSerializer, ReviewSerializer,\
                         ShoppingCartSerializer, ShoppingCartItemSerializer, AddShoppingCartItemSerializer,\
                         UpdateShoppingCartItemSerializer, NewOrderSerializer, UpdateShoppingOrderSerializer
from store.permissions import IsAdminOrReadOnly, FullPermissions
from django.contrib.auth.decorators import login_required
from intasend import APIService
import os

TEST_API_TOKEN = os.environ.get('TEST_API_TOKEN')
TEST_PUBLISHABLE_KEY = os.environ.get('TEST_PUBLISHABLE_KEY')


class SiteUserViewSet(ModelViewSet):
  """
    A viewset for viewing and editing SiteUser instances.

    Attributes:
    - queryset (QuerySet): The queryset for retrieving SiteUser instances.
    - serializer_class (Serializer): The serializer class to use
      for SiteUser instances.
    - permission_classes (list): The permission classes to apply to this viewset.

    Actions:
    - me (function): A custom action to retrieve or update the authenticated
      user's site user profile.
  """
  queryset = SiteUser.objects.all()
  serializer_class = SiteUserSerializer
  permission_classes = [IsAdminUser]

  @action(detail=False, methods=['GET', 'PUT'], permission_classes=[IsAuthenticated])
  def me(self, request):
    """
      Retrieve or update the authenticated user's site user profile.

      Methods:
      - GET: Returns the authenticated user's site user profile.
      - PUT: Updates the authenticated user's site user profile
        with the provided data.
    """
    siteuser = SiteUser.objects.get(user_id=request.user.id)
    if request.method == 'GET':
      serializer = SiteUserSerializer(siteuser)
      return Response(serializer.data)
       
    elif request.method == 'PUT':
      serializer = SiteUserSerializer(siteuser, data=request.data)
      serializer.is_valid(raise_exception=True)
      serializer.save()
      return Response(serializer.data)

class ProductsViewSet(ModelViewSet):
  """
    A viewset for viewing and editing Product instances.

    Attributes:
    - queryset (QuerySet): The queryset for retrieving Product instances.
    - serializer_class (Serializer): The serializer class to use
      for Product instances.
    - permission_classes (list): The permission classes to apply
      to this viewset.
  """
  queryset = Products.objects.all()
  serializer_class = ProductsSerializer
  permission_classes = [IsAdminOrReadOnly]


class ShoppingCartViewSet(CreateModelMixin,
                  RetrieveModelMixin,
                  DestroyModelMixin,
                  GenericViewSet):
    queryset = ShoppingCart.objects.prefetch_related('items__product').all()
    serializer_class = ShoppingCartSerializer


class ShoppingCartItemViewSet(ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return AddShoppingCartItemSerializer
        elif self.request.method == 'PATCH':
            return NewCartItemSerializer
        return ShoppingCartItemSerializer

    def get_serializer_context(self):
        return {'cart_id': self.kwargs['cart_pk']}

    def get_queryset(self):
        return ShoppingCartItem.objects \
            .filter(cart_id=self.kwargs['cart_pk']) \
            .select_related('product')



class CategoryViewSet(ModelViewSet):
  """
    A viewset for viewing and editing Category instances.

    Attributes:
    - queryset (QuerySet): The queryset for retrieving Category instances.
    - serializer_class (Serializer): The serializer class to use for
      Category instances.
    - permission_classes (list): The permission classes to apply to
      this viewset.
  """
  queryset = Category.objects.all()
  serializer_class = CategorySerializer
  permission_classes = [IsAdminOrReadOnly]

class ReviewViewSet(ModelViewSet):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        return Review.objects.filter(product_id=self.kwargs['product_pk'])

    def get_serializer_context(self):
        return {'product_id': self.kwargs['product_pk']}


class ShoppingOrderViewSet(ModelViewSet):
  http_method_names = ['get', 'post', 'patch', 'delete', 'head', 'options']
  def get_permissions(self):
    if self.request.method in ['PATCH', 'DELETE']:
      return [IsAdminUser()]
    return [IsAuthenticated()]

  def create(self, request, *args, **kwargs):
    serializer = NewOrderSerializer(
      data=request.data,
      context={'user_id': self.request.user.id}
      )
    serializer.is_valid(raise_exception=True)
    new_order = serializer.save()
    serializer = ShoppingOrderSerializer(new_order)
    return Response(serializer.data)
 

  def get_serializer_class(self):
    if self.request.method == 'POST':
      return NewOrderSerializer
    if self.request.method == 'PATCH':
      return UpdateShoppingOrderSerializer
    return ShoppingOrderSerializer

  def get_queryset(self):
    user = self.request.user
    if user.is_staff:
      return ShoppingOrder.objects.all()
    id = SiteUser.objects.only('id').get(user_id=user.id)
    return ShoppingOrder.objects.filter(siteuser_id=id)

class ShoppingOrderItemViewSet(ModelViewSet):
  """
    A viewset for viewing and editing ShoppingOrderItem instances.

    Attributes:
    - queryset (QuerySet): The queryset for retrieving ShoppingOrderItem
      instances.
    - serializer_class (Serializer): The serializer class to use for
      ShoppingOrderItem instances.
    - permission_classes (list): The permission classes to apply to
      this viewset.
  """
  queryset = ShoppingOrderItem.objects.all()
  serializer_class = ShoppingOrderItemSerializer
  permission_classes = [IsAuthenticated]

@login_required
def checkout(request, product_id):
    product = get_object_or_404(Products, id=product_id)
    user = request.user

    # Create or get the shopping order for the user with 'Pending' payment status
    shopping_order, _ = ShoppingOrder.objects.get_or_create(siteuser=user, payment_status='Pending')
    shopping_order.save()
    # Create or update the shopping order item
    order_item, created = ShoppingOrderItem.objects.get_or_create(
        order=shopping_order,  # Link to the shopping order
        products=product,  # Link to the product
        defaults={'quantity': 1, 'unit_price': product.unit_price}  # Default values for new item
    )
    if not created:
        order_item.quantity += 1  # Increase quantity if the item already exists
        order_item.save()

    context = {'orders': shopping_order, 'products': product}
    return render(request, 'store/shoppingcart.html', {'context': context})

@login_required
def purchase(request):
    user = request.user
    shopping_order = ShoppingOrder.objects.get(siteuser=user, payment_status='Pending')
    order_items = ShoppingOrderItem.objects.filter(order=shopping_order)
    service = APIService(token=TEST_API_TOKEN, publishable_key=TEST_PUBLISHABLE_KEY, test=True)
    response = service.collect.checkout(phone_number=254727563415,
                                        email=user.email, amount=10, currency="KES",
                                        comment="Service Fees", redirect_url="http://example.com/thank-you")
    return render(request, 'store/purchase.html', {'payment_url': response.get('url', '')})
