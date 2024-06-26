from django.contrib import admin
from django.conf import settings
from django.db import models


class SiteUser(models.Model):
    """
    Model representing a user
    """
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
    image = models.ImageField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    quantity_in_stock = models.IntegerField()

class Order(models.Model):
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


class OrderItem(models.Model):
    """
    OrderItem Model.
    """
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    products = models.ForeignKey(Products, on_delete=models.PROTECT, related_name='orderitems')
    order = models.ForeignKey(Order, on_delete=models.PROTECT)