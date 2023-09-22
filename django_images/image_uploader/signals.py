from django.db.models.signals import pre_delete
from django.dispatch import receiver
from .models import Image
import os


@receiver(pre_delete, sender=Image)
def delete_image_files(sender, instance, **kwargs):
    if instance.image:
        image_path = instance.image.path
        if os.path.exists(image_path):
            os.remove(image_path)