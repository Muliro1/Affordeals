from django.contrib.auth.models import AbstractUser #, User
from django.db import models
from django.contrib.auth import get_user_model
from PIL import Image

class User(AbstractUser):
  email = models.EmailField(unique=True)

class Profile(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE)
  image = models.ImageField(default='profile_pics/youtube.jpg', upload_to='profile_pics')
  def __str__(self):
    return f'{self.user.username} Profile'

  def save(self, *args, **kwargs):
    super().save(*args, **kwargs)
    img = Image.open(self.image.path)
    if img.height > 300 or img.width > 300:
      resized_img = (300, 300)
      img.thumbnail(resized_img)
      img.save(self.image.path)

