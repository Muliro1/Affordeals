from django.urls import path, include
from rest_framework_nested import routers
from .views import SiteUserViewSet


router = routers.DefaultRouter()
router.register('siteuser', SiteUserViewSet)

urlpatterns = [
  path('', include(router.urls)),
]