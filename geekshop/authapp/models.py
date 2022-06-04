from uuid import uuid4
from datetime import timedelta
from django.utils.timezone import now
from django.db import models
from django.contrib.auth.models import AbstractUser


def get_activation_key_expiry():
    return now() + timedelta(hours=48)


class ShopUser(AbstractUser):
    avatar = models.ImageField(upload_to="users_avatars", blank=True, null=True)
    age = models.PositiveIntegerField()

    activation_key = models.UUIDField(default=uuid4)
    activation_key_expiry = models.DateTimeField(default=get_activation_key_expiry)

    @property
    def is_activation_key_expired(self):
        return now() > self.activation_key_expiry

    def activation(self):
        self.is_active = True
        self.activation_key_expiry = now()
