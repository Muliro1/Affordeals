from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import User, profile



@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    """
    Create a profile for the user when a new user is created.

    Args:
        sender: The sender of the signal.
        instance: The instance of the User model.
        created: A boolean indicating whether the User instance was created.
        **kwargs: Additional keyword arguments.
    """
    # Check if the user instance was created
    if created:
        # Create a profile for the user
        profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    """
    Save the profile associated with the user instance.

    Args:
        sender: The sender of the signal.
        instance: The instance of the User model.
        **kwargs: Additional keyword arguments.
    """
    # Save the profile associated with the user instance
    # This is necessary to ensure that the profile is saved
    # whenever the user instance is saved
    instance.profile.save()
