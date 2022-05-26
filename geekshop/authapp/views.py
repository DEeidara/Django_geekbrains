from django.shortcuts import render, HttpResponseRedirect
from .forms import ShopUserLoginForm, ShopUserRegistrationForm, ShopUserEditForm
from django.contrib import auth
from django.urls import reverse
from django.contrib.auth.decorators import login_required


def login(request):
    login_form = ShopUserLoginForm(data=request.POST)
    if request.method == 'POST' and login_form.is_valid():
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)
        if user and user.is_active:
            auth.login(request, user=user),
            redirect_url = request.GET.get('next', reverse('index'))
            return HttpResponseRedirect(redirect_url)

    content = {'title': 'Login', 'login_form': login_form}
    return render(request, 'authapp/login.html', content)


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('index'))


def register(request):
    if request.method == 'POST':
        register_form = ShopUserRegistrationForm(request.POST, request.FILES)

        if register_form.is_valid():
            register_form.save()
            return HttpResponseRedirect(reverse('auth:login'))
    else:
        register_form = ShopUserRegistrationForm()

    content = {'title': 'Registration', 'register_form': register_form}
    return render(request, 'authapp/register.html', content)


@login_required
def edit(request):
    if request.method == 'POST':
        edit_form = ShopUserEditForm(
            request.POST, request.FILES, instance=request.user)
        if edit_form.is_valid():
            edit_form.save()
            return HttpResponseRedirect(reverse('auth:edit'))
    else:
        edit_form = ShopUserEditForm(instance=request.user)

    content = {'title': 'Edit', 'edit_form': edit_form}
    return render(request, 'authapp/edit.html', content)
