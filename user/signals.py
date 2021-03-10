from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import DineSafelyUser, User_Profile


@receiver(post_save, sender=DineSafelyUser)
def create_profile(sender, instance, created, **kwargs):
    if created:
        User_Profile.objects.create(user=instance)


@receiver(post_save, sender=DineSafelyUser)
def save_profile(sender, instance, **kwargs):
    instance.user_profile.save()
