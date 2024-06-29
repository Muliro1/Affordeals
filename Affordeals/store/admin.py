from django.contrib import admin
from django.db.models.aggregates import Count
from django.utils.html import format_html, urlencode
from .models import Products, Address, SiteUser, Category, Order, OrderItem
from django.urls import reverse


admin.site.register(Address)

@admin.register(Products)
class ProductsAdmin(admin.ModelAdmin):
    autocomplete_fields = ['category']
    list_display = ['name', 'unit_price', 'category_name']
    list_per_page = 10
    list_select_related = ['category']
    search_fields = ['name']

    def category_name(self, products):
        return products.category.name


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    autocomplete_fields = ['highlighted_product']
    list_display = ['name', 'products_count']
    search_fields = ['name']

    @admin.display(ordering='products_count')
    def products_count(self, category):
        url = (
            reverse('admin:store_products_changelist')
            + '?'
            + urlencode({
                'category__id': str(category.id)
            }))
        return format_html('<a href="{}">{} Products</a>', url, category.products_count)

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            products_count=Count('products')
        )


@admin.register(SiteUser)
class SiteUserAdmin(admin.ModelAdmin):
  list_display = ['first_name', 'last_name']
  list_select_related = ['user']
  search_fields = ['first_name__istartswith', 'last_name__istartswith']

  @admin.display(ordering='orders_count')
  def orders(self, siteuser):
    url = (
      reverse('admin:store_order_changelist')
      + '?'
      + urlencode({
        'siteuser__id': str(siteuser.id)
      })
    )
    return format_html('<a href="{}">{} Orders</a>', url, siteuser.orders_count)
  
  def get_queryset(self, request):
    return super().get_queryset(request).annotate(
      orders_count=Count('order')
    )

class OrderItemInline(admin.TabularInline):
    autocomplete_fields = ['products']
    min_num = 1
    max_num = 10
    model = OrderItem
    extra = 0

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
  autocomplete_fields = ['siteuser']
  list_display = ['id', 'created_at', 'siteuser']
  inlines = [OrderItemInline]