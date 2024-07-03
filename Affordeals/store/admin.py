from django.contrib import admin
from django.db.models.aggregates import Count
from django.utils.html import format_html, urlencode
from .models import Products, Address, SiteUser, Category, ShoppingOrder, ShoppingOrderItem, ShoppingCart, ShoppingCartItem 
from django.urls import reverse


@admin.register(Products)
class ProductsAdmin(admin.ModelAdmin):
    """
    Admin interface for managing Product objects.

    Configuration:
    - autocomplete_fields (list): Fields to use for autocomplete widgets.
    - list_display (list): Fields to display in the admin list view.
    - list_per_page (int): Number of items to display per page in the
      admin list view.
    - list_select_related (list): Related fields to fetch in the same
      database query.
    - search_fields (list): Fields to include in the search functionality.

    Methods:
    - category_name (function): Returns the name of the category for a
      given product.
    """
    autocomplete_fields = ['category']
    list_display = ['name', 'unit_price', 'category_name']
    list_per_page = 10
    list_select_related = ['category']
    search_fields = ['name']

    def category_name(self, products):
        return products.category.name


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """
    Admin interface for managing Category objects.

    Configuration:
    - autocomplete_fields (list): Fields to use for autocomplete widgets.
    - list_display (list): Fields to display in the admin list view.
    - search_fields (list): Fields to include in the search functionality.

    Methods:
    - products_count (function): Returns the number of products in a given category.
    - get_queryset (function): Customizes the query set to include the
      product count annotation.
    """
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
  """
    Admin interface for managing SiteUser objects.

    Configuration:
    - list_display (list): Fields to display in the admin list view.
    - list_select_related (list): Related fields to fetch in the
      same database query.
    - search_fields (list): Fields to include in the search functionality.

    Methods:
    - orders (function): Returns the number of orders for a given site user.
    - get_queryset (function): Customizes the query set to include the order
      count annotation.
  """
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
    """
    Inline admin interface for managing ShoppingOrderItem
    objects within an order.

    Configuration:
    - autocomplete_fields (list): Fields to use for autocomplete widgets.
    - min_num (int): Minimum number of items required.
    - max_num (int): Maximum number of items allowed.
    - model (class): The model to be managed.
    - extra (int): Number of extra empty forms to display.
    """
    autocomplete_fields = ['products']
    min_num = 1
    max_num = 10
    model = ShoppingOrderItem
    extra = 0

@admin.register(ShoppingOrder)
class OrderAdmin(admin.ModelAdmin):
  """
    Admin interface for managing ShoppingOrder objects.

    Configuration:
    - autocomplete_fields (list): Fields to use for autocomplete widgets.
    - list_display (list): Fields to display in the admin list view.
    - inlines (list): Inline admin interfaces to include.

    Fields:
    - id (UUID): A unique identifier for the order.
    - created_at (DateTime): The timestamp when the order was created.
    - siteuser (ForeignKey): Reference to the user who placed the order.
  """
  autocomplete_fields = ['siteuser']
  list_display = ['id', 'created_at', 'siteuser']
  inlines = [OrderItemInline]