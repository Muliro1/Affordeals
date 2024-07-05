from django.contrib.auth.models import AbstractUser #, User
from django.db import models
from django.contrib.auth import get_user_model

class User(AbstractUser):
  email = models.EmailField(unique=True)

class Profile(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE)
  image = models.ImageField(default='default.jpg', upload_to='profile_pics')
  def __str__(self):
    return f'{self.user.username} Profile'

