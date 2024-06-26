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
  """
    A viewset for viewing and editing ShoppingOrder instances.

    Attributes:
    - queryset (QuerySet): The queryset for retrieving ShoppingOrder
      instances.
    - serializer_class (Serializer): The serializer class to use for
      ShoppingOrder instances.
    - permission_classes (list): The permission classes to apply to
      this viewset.
  """
  queryset = ShoppingOrder.objects.all()
  serializer_class = ShoppingOrderSerializer
  permission_classes = [IsAuthenticated]


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

