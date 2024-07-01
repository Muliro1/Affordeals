from django.contrib.auth.models import AbstractUser, User
from django.db import models
from django.contrib.auth import get_user_model

# Class User:
#   Extends the AbstractUser model from django.contrib.auth.models
#   Adds an email field which is unique
#
# Fields:
#   email = models.EmailField(unique=True)

# This is a custom user model that extends the AbstractUser model provided by Django.
# It adds a profile image field to the user model.

class profile(models.Model):
  """
  Model representing a user profile.
  
  Fields:
  - user (OneToOneField): A one-to-one relationship with the Django user model.
  - image (ImageField): A field to store the user's profile image.
  
  Methods:
  - __str__(): Returns the username of the user.
  """
  user = models.OneToOneField(User, on_delete=models.CASCADE)
  image = models.ImageField(default='default.jpg', upload_to='profile_pics')
  
  def __str__(self):
    """
    Returns the username of the user.
    
    Returns:
    - str: The username of the user.
    """
    return f'{self.user.username} Profile'
