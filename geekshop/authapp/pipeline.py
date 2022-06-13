import requests


def get_user_info(user, response, *args, **kwargs):
    access_token = response["access_token"]

    vk_response = requests.get(
        f"https://api.vk.com/method/users.get?&access_token={access_token}&fields=bdate,sex&v=5.131"
    )
    user.profile.about = vk_response.text
    user.email = kwargs["details"]["email"]
    user.save()
