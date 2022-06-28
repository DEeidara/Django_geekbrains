import json
from django.conf import settings
from .models import Category

with open((settings.JSON_ROOT / "data.json"), "r", encoding="utf-8") as f:
    data_json = json.load(f)


def data(request):
    return {
        "menu": data_json["menu"],
        "social_links": data_json["social_links"],
    }


def basket(request):
    return {"basket": getattr(request.user, "basket", None)}


def categories(request):
    return {"categories": Category.objects.all()}
