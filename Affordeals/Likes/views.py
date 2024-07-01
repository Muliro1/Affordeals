from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser, DjangoModelPermissions
from rest_framework.response import Response
from rest_framework.decorators import action
from .serializers import LikesSerializer
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from .models import LikedItem

from store.permissions import IsAdminOrReadOnly, FullPermissions


class ProductsLikes(ModelViewSet):
    model = LikedItem
    serializer_class = LikesSerializer
    permission_classes = [IsAdminOrReadOnly]
    
    
    @action(detail=False, methods=['GET'], permission_classes=[IsAuthenticated])
    def Get_ProductsLikes(self, request):
       
        queryset = LikedItem.objects.filter(object_id=request.data, ordered=True)
    
        if queryset.exists():
            return Response(queryset)
        else:
            return Response([])
        
    @action(detail=False, methods=['GET'], permission_classes=[IsAuthenticated])
    def Get_ProductsLikes(self, request):
       
        queryset = LikedItem.objects.filter(object_id=request.data, ordered=True)
    
        if queryset.exists():
            return Response(queryset)
        else:
            return Response([])



