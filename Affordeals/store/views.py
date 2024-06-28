from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import action
from .serializers import SiteUserSerializer
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.mixins import RetrieveModelMixin, UpdateModelMixin,  CreateModelMixin, DestroyModelMixin
from .models import SiteUser
from .serializers import SiteUserSerializer

class SiteUserViewSet(CreateModelMixin, UpdateModelMixin, RetrieveModelMixin, GenericViewSet):
  queryset = SiteUser.objects.all()
  serializer_class = SiteUserSerializer

  @action(detail=False, methods=['GET', 'PUT'])
  def me(self, request):
    (customer, created) = SiteUser.objects.get_or_create(user_id=request.user.id)
    if request.method == 'GET':
      serializer = SiteUserSerializer(customer)
      return Response(serializer.data)
       
    elif request.method == 'PUT':
      serializer = SiteUserSerializer(customer, data=request.data)
      serializer.is_valid(raise_exception=True)
      serializer.save()
      return Response(serializer.data)