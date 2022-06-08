from django.core.management.base import BaseCommand
from authapp.models import ShopUserProfile, ShopUser


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        users = ShopUser.objects.all()
        for user in users:
            profile = ShopUserProfile.objects.filter(user=user).first()
            print(profile)
            if not profile:
                profile = ShopUserProfile(user=user)
                profile.save()
