from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser, DjangoModelPermissions
from rest_framework.response import Response
from rest_framework.decorators import action
from .serializers import SiteUserSerializer
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from .models import SiteUser, Products, Category, ShoppingOrder, ShoppingOrderItem
from .serializers import SiteUserSerializer, ProductsSerializer, CategorySerializer,\
                         ShoppingOrderSerializer, ShoppingOrderItemSerializer
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
  
  @action(detail=False, methods=['PUT'], permission_classes=[IsAuthenticated])
  def Add_Product(self, request):
    (products, created) = Products.objects.get_or_create(name=request.data.name)
    serializer = ProductsSerializer(products, data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data)
  
  @action(detail=False, methods=['GET'], permission_classes=[IsAuthenticated])
  def Get_Product(self, request):
    (products, created) = SiteUser.objects.get_or_create(name=request.data.name)
    serializer = ProductsSerializer(products)
    return Response(serializer.data)



class CategoryViewSet(ModelViewSet):
  queryset = Category.objects.all()
  serializer_class = CategorySerializer
  permission_classes = [IsAdminOrReadOnly]
  
  @action(detail=False, methods=['PUT'], permission_classes=[IsAuthenticated])
  def Add_Category(self, request):
    (category, created) = Category.objects.get_or_create(name=request.data.name)
    serializer = CategorySerializer(category, data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data)
  
  @action(detail=False, methods=['GET'], permission_classes=[IsAuthenticated])
  def Get_Category(self, request):
    (category, created) = Category.objects.get_or_create(name=request.data.name)
    serializer = ProductsSerializer(category)
    return Response(serializer.data)


class ShoppingOrderViewSet(ModelViewSet):
  queryset = ShoppingOrder.objects.all()
  serializer_class = ShoppingOrderSerializer
  permission_classes = [IsAuthenticated]


class ShoppingOrderItemViewSet(ModelViewSet):
  queryset = ShoppingOrderItem.objects.all()
  serializer_class = ShoppingOrderItemSerializer
  permission_classes = [IsAuthenticated]

