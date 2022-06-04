from django.shortcuts import render, HttpResponseRedirect
from .forms import ShopUserLoginForm, ShopUserRegistrationForm, ShopUserEditForm
from django.contrib import auth
from django.urls import reverse
from .utils import send_verification_mail
from django.contrib.auth.decorators import login_required
from .models import ShopUser


def login(request):
    form = ShopUserLoginForm(data=request.POST)
    if request.method == "POST" and form.is_valid():
        username = request.POST["username"]
        password = request.POST["password"]

        user = auth.authenticate(username=username, password=password)
        if user and user.is_active:
            auth.login(request, user=user),
            redirect_url = request.GET.get("next", reverse("index"))
            return HttpResponseRedirect(redirect_url)

    content = {"title": "Login", "form": form}
    return render(request, "authapp/login.html", content)


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    form = ShopUserRegistrationForm()
    if request.method == "POST":
        form = ShopUserRegistrationForm(request.POST, request.FILES)

        if form.is_valid():
            user = form.save()
            send_verification_mail(user)
            return HttpResponseRedirect(reverse("auth:login"))

    content = {"title": "Registration", "form": form}
    return render(request, "authapp/register.html", content)


@login_required
def edit(request):
    form = ShopUserEditForm(instance=request.user)
    if request.method == "POST":
        form = ShopUserEditForm(request.POST, request.FILES, instance=request.user)

        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("auth:edit"))

    content = {"title": "Edit", "form": form}
    return render(request, "authapp/edit.html", content)


def verify(request, email, key):
    try:
        user = ShopUser.objects.get(email=email, activation_key=key)
        if user.is_activation_key_expired:
            return render(
                request,
                "authapp/verification.html",
                context={"message": "Activation key has expired"},
            )
        user.activation()
        user.save()
        return render(
            request,
            "authapp/verification.html",
            context={"message": "Success!"},
        )
    except ShopUser.DoesNotExist:
        return render(
            request,
            "authapp/verification.html",
            context={"message": "Verification failed"},
        )
