from django.contrib import admin
from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models
from uuid import uuid4


class SiteUser(models.Model):
    """
    Model representing a user
    """
    birth_date = models.DateField(null=True, blank=True)
    phone_number = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return '{} {}'.format(self.user.first_name, self.user.last_name)
    
    @admin.display(ordering='user__first_name')
    def first_name(self):
        return self.user.first_name

    @admin.display(ordering='user__last_name')
    def last_name(self):
        return self.user.last_name

    class Meta:
        ordering = ['user__first_name', 'user__last_name']

class Address(models.Model):
    """
    Model representing user address
    """
    siteuser = models.ForeignKey(SiteUser, on_delete=models.CASCADE)
    country = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    street_number = models.CharField(max_length=100)
    address_line_1 = models.CharField(max_length=100)


class Category(models.Model):
    """
    Model representing products categories
    """
    name = models.CharField(max_length=100)
    highlighted_product = models.ForeignKey(
        'Products', on_delete=models.SET_NULL,
        null = True,
        related_name='+',
        blank=True
    )


class Products(models.Model):
    """
    Model representing products
    """
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    image = models.ImageField(
        upload_to='images/',  # Specify the upload directory
        blank=True,           # Allow the field to be empty
        null=True,            # Allow the database field to be null
        help_text='Upload an image file (optional)'  # Optional help text for admin interface
        )
    description = models.TextField()
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)
    quantity_in_stock = models.IntegerField()

class ShoppingOrder(models.Model):
    """
    Order model.
    """
    PAYMENT_STATUS_PENDING = 'P'
    PAYMENT_STATUS_COMPLETE = 'C'
    PAYMENT_STATUS_FAILED = 'F'

    PAYMENT_STATUS_CHOICES = [
        (PAYMENT_STATUS_PENDING, 'Pending'),
        (PAYMENT_STATUS_COMPLETE, 'Complete'),
        (PAYMENT_STATUS_FAILED, 'Failed')
    ]
    created_at = models.DateTimeField(auto_now_add=True)
    payment_status = models.CharField(max_length=1,
                        choices=PAYMENT_STATUS_CHOICES,
                        default=PAYMENT_STATUS_PENDING)
    siteuser = models.ForeignKey(SiteUser, on_delete=models.PROTECT)

    class Meta:
        permissions = [
            ('cancel_order', 'Can cancel order')
        ]


class ShoppingOrderItem(models.Model):
    """
    OrderItem Model.
    """
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=8, decimal_places=2)
    products = models.ForeignKey(Products, on_delete=models.PROTECT, related_name='orderitems')
    order = models.ForeignKey(ShoppingOrder, on_delete=models.PROTECT, related_name='items')


class ShoppingCart(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4)
    created_at = models.DateTimeField(auto_now_add=True)


class ShoppingCartItem(models.Model):
    cart = models.ForeignKey(ShoppingCart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1)]
    )

    class Meta:
        unique_together = [['cart', 'product']] #the same product cannot be added multiple times to the same cart
                                                # no duplicate product entries in the same cart

class Review(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    product = models.ForeignKey(Products, on_delete=models.CASCADE, related_name='reviews')
