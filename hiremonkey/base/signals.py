#
# @receiver(post_delete, sender=JobSeeker)
# @receiver(post_delete, sender=Recruiter)
# def delete_orphaned_profile_references(sender, instance, **kwargs):
#     # Get the ContentType for the deleted instance
#     content_type = ContentType.objects.get_for_model(instance)
#
#     # Delete ProfileReference objects that reference the deleted instance
#     ProfileReference.objects.filter(
#         content_type=content_type, object_id=instance.id
#     ).delete()
#
# @receiver(post_save, sender=User)
# def grant_skill_add_permission(sender, instance, created, **kwargs):
#     if created:  # Only when a new user is created
#         content_type = ContentType.objects.get_for_model(Skill)
#         permission = Permission.objects.get(
#             codename='add_skill',
#             content_type=content_type,
#         )
#         instance.user_permissions.add(permission)
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver

from .models import Profile, UserSession


@receiver(post_save, sender=User)
def manage_profile(sender, instance, created, **kwargs):
    if created:
        # Create Profile, UserSession
        Profile.objects.create(user=instance)
        UserSession.objects.create(user=instance)
    else:
        if hasattr(instance, "profile"):
            instance.profile.save()
        if hasattr(instance, "user_session"):
            instance.user_session.save()
