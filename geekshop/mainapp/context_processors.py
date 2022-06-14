import json
from django.conf import settings
from .models import Category

with open((settings.JSON_ROOT / "data.json"), "r", encoding="utf-8") as f:
    data_js = json.load(f)


def data(request):
    return {
        "menu": data_js["menu"],
        "social_links": data_js["social_links"],
    }


def basket(request):
    return {"basket": getattr(request.user, "basket", None)}


def categories(request):
    return {"categories": Category.objects.all()}
