import debug_toolbar
from django.contrib import admin
from django.urls import path, include
from main import views as user_views
from store import views as store_views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', user_views.register, name='register'),
    path('', user_views.home, name='home'),
    path('account/', user_views.account, name='account'),
    path('login/', auth_views.LoginView.as_view(template_name='main/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='main/logout.html'), name='logout'),
    
    path('password-reset/',
         auth_views.PasswordResetView.as_view(template_name='main/password_reset.html'),
         name='password_reset'),
    path('password-reset-done/',
         auth_views.PasswordResetDoneView.as_view(template_name='main/password_reset_done.html'),
         name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='main/password_reset_confirm.html',
         ), name='password_reset_confirm'),
    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name='main/password_reset_complete.html'),
         name='password_reset_complete'),
    
    path('about/', user_views.about, name='about'),
    path('products/', user_views.product_view, name='product'),
    path('', user_views.home, name='home'),
    path('purchase/', store_views.purchase, name='purchase'),

    path('checkout/<int:product_id>/', store_views.checkout, name='checkout'),
    path('store/', include('store.urls')),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    path('djdt/', include('debug_toolbar.urls', namespace='djdt')),
    path('success/', store_views.success, name='success'),
    path('cancel/', store_views.cancel, name='cancel'),

]  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)