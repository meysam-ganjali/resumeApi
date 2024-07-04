from django.db.models.signals import post_delete
from django.dispatch import receiver
from .models import Blog


@receiver(post_delete, sender=Blog)
def delete_cover_image(sender, instance, **kwargs):
    instance.cover_image.delete(False)



