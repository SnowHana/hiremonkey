from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver

from .models import Profile, UserSession


@receiver(post_save, sender=User)
def manage_profile(sender, instance, created, **kwargs):
    if created:
        # Create Profile and UserSession when a new User is created
        Profile.objects.create(user=instance)
        UserSession.objects.create(user=instance)
    else:
        # For existing users, just save their profile and user session
        if not hasattr(instance, "profile"):
            # If profile does not exist, create it
            Profile.objects.create(user=instance)
        else:
            instance.profile.save()  # Save if the profile exists

        if not hasattr(instance, "user_session"):
            UserSession.objects.create(user=instance)
        else:
            instance.user_session.save()  # Save user session if it exists


from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver

from .models import Profile, UserSession


@receiver(post_save, sender=User)
def manage_profile(sender, instance, created, **kwargs):
    if created:
        # Create Profile when a new User is created
        Profile.objects.create(user=instance)
        UserSession.objects.create(user=instance)
    else:

        instance.profile.save()  # Save if the profile exists
        instance.user_session.save()  # Save user session if it exists
