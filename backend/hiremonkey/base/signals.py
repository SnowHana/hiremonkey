from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.contrib.contenttypes.models import ContentType
from .models import JobSeeker, ProfileReference, Recruiter, Skill
from django.db.models.signals import post_save
from django.contrib.auth.models import User, Permission


@receiver(post_delete, sender=JobSeeker)
@receiver(post_delete, sender=Recruiter)
def delete_orphaned_profile_references(sender, instance, **kwargs):
    # Get the ContentType for the deleted instance
    content_type = ContentType.objects.get_for_model(instance)

    # Delete ProfileReference objects that reference the deleted instance
    ProfileReference.objects.filter(
        content_type=content_type, object_id=instance.id
    ).delete()
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