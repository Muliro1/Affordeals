from django.urls import path, include
from rest_framework_nested import routers
from .views import SiteUserViewSet, ProductsViewSet, CategoryViewSet, ShoppingOrderViewSet,\
                   ShoppingOrderItemViewSet, ShoppingCartItemViewSet, ShoppingCartViewSet, ReviewViewSet


router = routers.DefaultRouter()
router.register('product', ProductsViewSet, basename='product')
router.register('category', CategoryViewSet)
router.register('orders', ShoppingOrderViewSet, basename='orders')

router.register('carts', ShoppingCartViewSet, basename='carts')
router.register('siteuser', SiteUserViewSet)


product_router = routers.NestedDefaultRouter(router, 'product', lookup='products')
product_router.register('reviews', ReviewViewSet, basename='products-reviews' )

cartRouter = routers.NestedDefaultRouter(router, 'carts', lookup='cart')
cartRouter.register('cartitems', ShoppingCartItemViewSet, basename='cart-cartitems')


urlpatterns = [
  path('', include(router.urls)),
  path('', include(product_router.urls)),
  path('', include(cartRouter.urls)),
]