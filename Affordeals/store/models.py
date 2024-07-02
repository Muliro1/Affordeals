from django.contrib import admin
from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models
from uuid import uuid4
from main.models import User, profile


class SiteUser(models.Model):
    """
    Model representing a user.

    Fields:
    - birth_date (DateField): The birth date of the user,
      which can be null or blank.
    - phone_number (CharField): The phone number of the user with a
      maximum length of 20 characters.
    - created_at (DateTimeField): The date and time when the user was
      created, automatically set on creation.
    - updated_at (DateTimeField): The date and time when the user was
      last updated, automatically updated.
    - user (OneToOneField): A one-to-one relationship with the
      Django user model, ensuring each user has one profile.

    Methods:
    - __str__(): Returns the user's first and last name as a string.
    - first_name(): Displays the user's first name in the admin
      interface, ordered by 'user__first_name'.
    - last_name(): Displays the user's last name in the admin interface,
      ordered by 'user__last_name'.

    Meta:
    - ordering: Orders the users by first name and last name in ascending order

    The SiteUser model represents additional user information
    such as birth date and phone number, linked to the Django user model.
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
    Model represents a user's address with fields for country, state, city,
    street number, 
    and the first line of the address, linked to a specific user.
    """
    siteuser = models.ForeignKey(SiteUser, on_delete=models.CASCADE)
    country = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    street_number = models.CharField(max_length=100)
    address_line_1 = models.CharField(max_length=100)


class Category(models.Model):
    """
    Model representing product categories.

    Fields:
    - name (CharField): The name of the category with a maximum
      length of 100 characters.
    - highlighted_product (ForeignKey): An optional reference to a product
      that is highlighted in this category. 
      This field can be null or blank, and uses 'Products' model. Deletion of
      the product sets this field to null.
    """
    name = models.CharField(max_length=100)
    highlighted_product = models.ForeignKey(
        'Products', on_delete=models.SET_NULL,
        null = True,
        related_name='+',
        blank=True
    )

    def __str__(self) -> str:
        return self.name


class Products(models.Model):
    """
    Model representing products.

    Fields:
    - name (CharField): The name of the product with a maximum
      length of 100 characters.
    - category (ForeignKey): A reference to the Category model,
      ensuring category integrity on deletion.
    - image (ImageField): An optional image of the product,
      stored in the 'images/' directory.
    - description (TextField): A detailed description of the product.
    - unit_price (DecimalField): The price per unit of the product, with up
      to 6 digits and 2 decimal places.
    - quantity_in_stock (IntegerField): The number of units available in stock.
    """
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    image = models.ImageField(
        upload_to='media/',
        blank=True,           # Allow the field to be empty
        null=True,            # Allow the database field to be null
        help_text='Upload an image file (optional)'  # Optional help text for admin interface
        )
    description = models.TextField()
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)
    quantity_in_stock = models.IntegerField()
    

    def __str__(self) -> str:
        return self.name

class ShoppingOrder(models.Model):
    """
    This class represents an Order model.
    It stores information about an order made by a SiteUser.
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
    siteuser = models.ForeignKey(User, on_delete=models.PROTECT)

    class Meta:
        permissions = [
            ('cancel_order', 'Can cancel order')
        ]

    def __str__(self) -> str:
        return f"Order {self.id}"


class ShoppingOrderItem(models.Model):
    """
    Represents an item in an order.

    Fields:
    - quantity (PositiveIntegerField): The quantity of the product in the order.
    - unit_price (DecimalField): The unit price of the product.
    - products (ForeignKey): The product associated with this order item.
    - order (ForeignKey): The order this item belongs to.
    """
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=8, decimal_places=2)
    products = models.ForeignKey(Products, on_delete=models.PROTECT, related_name='orderitems')
    order = models.ForeignKey(ShoppingOrder, on_delete=models.PROTECT, related_name='items')

    def __str__(self) -> str:
        return f"Order Item {self.id}" 


class ShoppingCart(models.Model):
    """
    Represents a shopping cart used by customers to store items
    they intend to purchase.

    Fields:
    - id (UUID): A unique identifier for the shopping cart.
    - created_at (DateTime): The timestamp when the shopping cart was created.
    """
    id = models.UUIDField(primary_key=True, default=uuid4)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"Cart {self.id}"


class ShoppingCartItem(models.Model):
    """
    Represents an item in a shopping cart.
    
    Fields:
    - cart (ForeignKey): The shopping cart this item belongs to.
    - product (ForeignKey): The product associated with this item.
    - quantity (PositiveSmallIntegerField): The quantity of the
    product in the cart

    Meta:
    unique_together = [['cart', 'product']] ensures that each product can only
    be added to a specific cart once, preventing duplicates.
    """

    cart = models.ForeignKey(ShoppingCart, on_delete=models.CASCADE, related_name='cartitems')
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1)]
    )

    class Meta:
        unique_together = [['cart', 'product']]




class Review(models.Model):
    """
    Represents a review for a product.
    
    Fields:
    - name (CharField): The name of the reviewer.
    - description (TextField): The text of the review.
    - date (DateTimeField): The timestamp when the review was created.
    - product (ForeignKey): The product associated with this review.
    
    The product field uses the on_delete=models.CASCADE option to ensure
    that when a product is deleted, its associated reviews are also deleted
    """
    name = models.CharField(max_length=255)
    description = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    product = models.ForeignKey(Products, on_delete=models.CASCADE, related_name='reviews')
