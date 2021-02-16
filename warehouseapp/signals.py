from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import *
@receiver(post_save, sender=User)
def create_issue(sender, instance, created, **kwargs):

    if created:
        Product.objects.create(user=instance)