from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.core.exceptions import ObjectDoesNotExist
from .models import Profile, UserSession


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        UserSession.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()
    instance.usersession.save()


# @receiver(post_save, sender=User)
# def manage_profile(sender, instance, created, **kwargs):
#     if created:
#         try:
#             Profile.objects.get(user=instance)
#         # Create Profile when a new User is created
#         except ObjectDoesNotExist:
#             # Does not exist
#             Profile.objects.create(user=instance)
#         try:
#             UserSession.objects.get(user=instance)
#         except ObjectDoesNotExist:
#             UserSession.objects.create(user=instance)
#     else:

#         instance.profile.save()  # Save if the profile exists
#         instance.user_session.save()  # Save user session if it exists
