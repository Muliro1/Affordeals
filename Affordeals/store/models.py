from django.db import models


# Create your models here.
class SiteUser(models.Model):
    """
    Model representing a user
    """
    first_name = models.CharField(max_length=100, default='')
    last_name = models.CharField(max_length=100, default='')
    email = models.EmailField(max_length=255)
    phone_number = models.CharField(max_length=20)
    password = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Address(models.Model):
    """
    Model representing user address
    """
    user_id = models.ForeignKey(SiteUser, on_delete=models.CASCADE)
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


class Products(models.Model):
    """
    Model representing products
    """
    name = models.CharField(max_length=100)
    category_id = models.ForeignKey(Category, on_delete=models.PROTECT)
    image = models.ImageField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    quantity_in_stock = models.IntegerField()
    discount = models.DecimalField(max_digits=3, decimal_places=2)
    # options = models.

