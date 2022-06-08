import requests


# так и не разобрался как это сделать, жаль что ни в вебинаре,
# ни в методичке четко не объяснено
def get_user_info(user, response, *args, **kwargs):
    access_token = response["access_token"]

    vk_response = requests.get(
        f"https://api.vk.com/method/account.getProfileInfo?&access_token={access_token}v=5.131"
    )

    user.profile.about = vk_response.text
    user.profile.save()
    return {}
