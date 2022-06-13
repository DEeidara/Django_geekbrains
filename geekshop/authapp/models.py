from uuid import uuid4
from datetime import timedelta
from django.utils.timezone import now
from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import AbstractUser
from django.dispatch import receiver


def get_activation_key_expiry():
    return now() + timedelta(hours=48)


class ShopUser(AbstractUser):
    avatar = models.ImageField(upload_to="users_avatars", blank=True, null=True)
    age = models.PositiveIntegerField(default=18)

    activation_key = models.UUIDField(default=uuid4)
    activation_key_expiry = models.DateTimeField(default=get_activation_key_expiry)

    @property
    def is_activation_key_expired(self):
        return now() > self.activation_key_expiry

    def activation(self):
        self.is_active = True
        self.activation_key_expiry = now()


class ShopUserProfile(models.Model):
    GENDERS = [
        ("M", "Male"),
        ("F", "Female"),
        ("O", "Other"),
    ]

    user = models.OneToOneField(
        ShopUser, related_name="profile", on_delete=models.CASCADE
    )
    about = models.TextField(blank=True)
    gender = models.CharField(max_length=1, choices=GENDERS)

    @receiver(post_save, sender=ShopUser)
    def update_user_profile(sender, instance, created, **kwargs):
        if created:
            profile = ShopUserProfile(user=instance)
            profile.save()
        else:
            instance.profile.save()
