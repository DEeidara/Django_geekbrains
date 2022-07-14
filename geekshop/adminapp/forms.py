from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.forms import (
    TextInput,
    EmailInput,
    CharField,
    PasswordInput,
    ModelForm,
    IntegerField,
)
from django.forms.widgets import HiddenInput
from authapp.models import ShopUser
from mainapp.models import Category, Product

admin_form_widgets = {
    "username": TextInput(attrs={"class": "form-control", "placeholder": "Username"}),
    "first_name": TextInput(attrs={"class": "form-control", "placeholder": "John"}),
    "last_name": TextInput(attrs={"class": "form-control", "placeholder": "Johnson"}),
    "email": EmailInput(
        attrs={"class": "form-control", "placeholder": "example@gmail.com"}
    ),
    "age": TextInput(attrs={"class": "form-control", "placeholder": "Age"}),
}


class ShopUserRegistrationForm(UserCreationForm):
    password1 = CharField(
        label="Password",
        widget=PasswordInput(
            attrs={"class": "form-control", "placeholder": "Password"}
        ),
    )
    password2 = CharField(
        label="Confirm password",
        widget=PasswordInput(
            attrs={"class": "form-control", "placeholder": "Password"}
        ),
    )

    class Meta:
        model = ShopUser
        fields = (
            "username",
            "first_name",
            "last_name",
            "password1",
            "password2",
            "email",
            "age",
            "avatar",
        )


class ShopUserEditForm(UserChangeForm):
    class Meta:
        model = ShopUser
        fields = (
            "username",
            "first_name",
            "last_name",
            "email",
            "age",
            "avatar",
            "is_active",
        )


class CategoryCreateEditForm(ModelForm):
    class Meta:
        model = Category
        fields = "__all__"

    discount = IntegerField(required=False, min_value=0, max_value=100, initial=0)


class ProductCreateEditForm(ModelForm):
    class Meta:
        model = Product
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["category"].widget = HiddenInput()
