from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import SiteUser

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_customer(sender, **kwargs):  
  if kwargs['created']:
    SiteUser.objects.create(user=kwargs['instance'])