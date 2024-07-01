from django.urls import path, include
from rest_framework_nested import routers
from .views import  ProductsLikes


router = routers.DefaultRouter()
router.register('likes', ProductsLikes.Get_ProductsLikes)



urlpatterns = [
  path('', include(router.urls)),
]