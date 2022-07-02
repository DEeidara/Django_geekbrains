from datetime import datetime
from django.conf import settings
import requests
from authapp.models import ShopUserProfile
from social_core.exceptions import AuthForbidden


def get_user_info(backend, user, response, *args, **kwargs):
    if backend.name != "vk-oauth2":
        return

    access_token = response["access_token"]

    vk_response = requests.get(
        f"https://api.vk.com/method/users.get?&access_token={access_token}&fields=bdate,sex,about,photo_max_orig&v=5.131"
    )

    if vk_response.status_code != 200:
        return

    vk_data = vk_response.json()["response"][0]
    user.email = kwargs["details"]["email"]

    if "sex" in vk_data:
        if vk_data["sex"] == 1:
            user.profile.gender = ShopUserProfile.FEMALE
        elif vk_data["sex"] == 2:
            user.profile.gender = ShopUserProfile.MALE
        else:
            user.profile.gender = ShopUserProfile.OTHER

    if "about" in vk_data:
        user.profile.about = vk_data["about"]

    if "bdate" in vk_data:
        bdate = datetime.strptime(vk_data["bdate"], "%d.%m.%Y").date()
        age = datetime.now().year - bdate.year
        if age < 18:
            user.delete()
            raise AuthForbidden("social_core.backends.vk.VKOAuth2")
        user.age = age

    if "photo_max_orig" in vk_data:
        avatar_url = vk_data["photo_max_orig"]
        avatar_response = requests.get(avatar_url)
        avatar_path = f"{settings.MEDIA_ROOT}/users_avatars/{user.pk}.jpg"
        with open(avatar_path, "wb") as avatar_file:
            avatar_file.write(avatar_response.content)

        user.avatar = f"users_avatars/{user.pk}.jpg"

    user.save()
