from django.urls import path, include
from rest_framework_nested import routers
from .views import SiteUserViewSet, ProductsViewSet, CategoryViewSet


router = routers.DefaultRouter()
router.register('siteuser', SiteUserViewSet)
router.register('product', ProductsViewSet, basename='products')
router.register('category', CategoryViewSet)

urlpatterns = [
  path('', include(router.urls)),
]