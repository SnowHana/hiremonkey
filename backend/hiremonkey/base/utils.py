import random
from django.template.defaultfilters import slugify


def slugify_instance_title(instance, save=False, new_slug=None):
    if new_slug is not None:
        slug = new_slug
    else:
        slug = slugify(f"{instance.title}")
    Klass = instance.__class__
    # Check if slug alr exists using recursion
    qs = Klass.objects.filter(slug=slug).exclude(id=instance.id)
    if qs.exists():
        # NOTE: Think of better logic lol
        rand_int = random.randint(300_000, 500_000) # random characters (to prevent duplicates)
        slug = f"{slug}-{rand_int}"
        return slugify_instance_title(instance, save=save, new_slug=slug)
    instance.slug = slug
    # Save if needed
    if save:
        instance.save()
    return instance
