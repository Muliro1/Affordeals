"""
URL configuration for Affordeals project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import debug_toolbar
from django.contrib import admin
from django.urls import path, include
from main import views as user_views
#from main.views import ProductsViewSet  # newly added
from store import views as store_views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
#from rest_framework_nested import routers # added


admin.site.site_header = 'Affordeal Site'
admin.site.index_title = 'Admin Nathan'

#router = routers.DefaultRouter() #added
 
#router.register('product', ProductsViewSet, basename='product')  #added


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', user_views.home, name='home'),
    path('account/', user_views.account, name='account'),
    path('login/', auth_views.LoginView.as_view(template_name='main/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='main/logout.html'), name='logout'),
    path('about/', user_views.about, name='about'),
    path('products/', user_views.product_view, name='product'),
    path('purchase/', store_views.purchase, name='purchase'),
    #path('/product', include(router.urls)), #added
    path('checkout/<int:product_id>/', store_views.checkout, name='checkout'),
    path('store/', include('store.urls')),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    path('djdt/', include('debug_toolbar.urls', namespace='djdt')),
    path('success/', store_views.success, name='success'),
    path('cancel/', store_views.cancel, name='cancel'),
    #path('create-payment-intent/', store_views.create_payment_intent, name='create-payment-intent'),
]  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
