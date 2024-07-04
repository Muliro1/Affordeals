from django.urls import path, include
from rest_framework_nested import routers
from .views import SiteUserViewSet, ProductsViewSet, CategoryViewSet, ShoppingOrderViewSet,\
                   ShoppingOrderItemViewSet


router = routers.DefaultRouter()
router.register('siteuser', SiteUserViewSet)
router.register('getproduct', ProductsViewSet.Get_Product)
router.register('addproduct', ProductsViewSet.Add_Product)
router.register('category', CategoryViewSet)
router.register('order', ShoppingOrderViewSet)
router.register('items', ShoppingOrderItemViewSet)



urlpatterns = [
  path('', include(router.urls)),
]