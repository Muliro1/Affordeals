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
import requests

TEST_PUBLISHABLE_KEY = 'ISPubKey_test_da0cd304-2ffc-4197-b713-90b18c1a33e8'
TEST_API_TOKEN = 'ISSecretKey_test_c0c0845b-c2c2-45c4-826b-1c4798d66bcf'
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

def checkout(request):
  return render(request, 'store/shoppingcart.html')
class ReviewViewSet(ModelViewSet):
  queryset = Review.objects.all()
  serializer_class = ReviewSerializer


class ShoppingCartViewSet(CreateModelMixin, RetrieveModelMixin,
                          DestroyModelMixin, GenericViewSet):
  queryset = ShoppingCart.objects.prefetch_related('cartitems__product').all()
  serializer_class = ShoppingCartSerializer

class ShoppingCartItemViewSet(ModelViewSet):
  http_method_names = ['get', 'post', 'patch', 'delete']
  def get_serializer_class(self):
    if self.request.method == 'POST':
      return AddShoppingCartItemSerializer
    elif self.request.method == 'PATCH':
      return UpdateShoppingCartItemSerializer
    return ShoppingCartItemSerializer

  def get_queryset(self):
    return ShoppingCartItem.objects.\
           filter(cart_id=self.kwargs['cart_pk']).select_related('product')
  
  def get_serializer_context(self):
    return {'cart_id': self.kwargs['cart_pk']}
