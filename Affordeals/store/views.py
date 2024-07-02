from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser, DjangoModelPermissions
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, DestroyModelMixin
from .serializers import SiteUserSerializer
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from .models import SiteUser, Products, Category, ShoppingOrder, ShoppingOrderItem, Review, ShoppingCart, ShoppingCartItem
from .serializers import SiteUserSerializer, ProductsSerializer, CategorySerializer,\
                         ShoppingOrderSerializer, ShoppingOrderItemSerializer, ReviewSerializer,\
                         ShoppingCartSerializer, ShoppingCartItemSerializer, AddShoppingCartItemSerializer,\
                         UpdateShoppingCartItemSerializer, NewOrderSerializer
from store.permissions import IsAdminOrReadOnly, FullPermissions


class SiteUserViewSet(ModelViewSet):
  queryset = SiteUser.objects.all()
  serializer_class = SiteUserSerializer
  permission_classes = [IsAdminUser]


  @action(detail=False, methods=['GET', 'PUT'], permission_classes=[IsAuthenticated])
  def me(self, request):
    (siteuser, created) = SiteUser.objects.get_or_create(user_id=request.user.id)
    if request.method == 'GET':
      serializer = SiteUserSerializer(siteuser)
      return Response(serializer.data)
       
    elif request.method == 'PUT':
      serializer = SiteUserSerializer(siteuser, data=request.data)
      serializer.is_valid(raise_exception=True)
      serializer.save()
      return Response(serializer.data)

class ProductsViewSet(ModelViewSet):
  queryset = Products.objects.all()
  serializer_class = ProductsSerializer
  permission_classes = [IsAdminOrReadOnly]


class CategoryViewSet(ModelViewSet):
  queryset = Category.objects.all()
  serializer_class = CategorySerializer
  permission_classes = [IsAdminOrReadOnly]

class ShoppingOrderViewSet(ModelViewSet):
  #serializer_class = ShoppingOrderSerializer
  permission_classes = [IsAuthenticated]

  def get_serializer_class(self):
    if self.request.method == 'POST':
      return NewOrderSerializer
    return ShoppingOrderSerializer

  def get_queryset(self):
    if self.request.user.is_staff:
      return ShoppingOrder.objects.all()
    (siteuser_id, created) = SiteUser.objects.only('id').get_or_create(user_id=self.request.user.id)
    return SiteUser.objects.filter(siteuser_id=siteuser_id)
  

class ShoppingOrderItemViewSet(ModelViewSet):
  queryset = ShoppingOrderItem.objects.all()
  serializer_class = ShoppingOrderItemSerializer
  permission_classes = [IsAuthenticated]

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
  
  

