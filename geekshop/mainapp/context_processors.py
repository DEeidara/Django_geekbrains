import json
from django.conf import settings
from .models import Category
from django.core.cache import cache
from django.conf import settings
import os


def get_links_menu():
    if settings.LOW_CACHE:
        key = "links_menu"
        links_menu = cache.get(key)
        if links_menu is None:
            links_menu = Category.objects.filter(is_active=True)
            cache.set(key, links_menu)
        return links_menu
    else:
        return Category.objects.filter(is_active=True)


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
    return {"categories": get_links_menu()}
