from django.contrib.auth.forms import (
    AuthenticationForm,
    UserCreationForm,
    UserChangeForm,
)
from django.forms import HiddenInput
from django.core.exceptions import ValidationError
from .models import ShopUser, ShopUserProfile


class ShopUserLoginForm(AuthenticationForm):
    class Meta:
        model = ShopUser
        fields = ("username", "password")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs["class"] = "form-control"


class ShopUserRegistrationForm(UserCreationForm):
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

    def save(self, commit=True):
        user = super().save()
        user.is_active = False
        user.save()
        return user

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs["class"] = "form-control"
            field.help_text = ""

    def clean_age(self):
        data = self.cleaned_data["age"]
        if data < 18:
            raise ValidationError("You are too young")
        return data


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
            "password",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs["class"] = "form-control"
            field.help_text = ""
            if field_name == "password":
                field.widget = HiddenInput()

    def clean_age(self):
        data = self.cleaned_data["age"]
        if data < 18:
            raise ValidationError("You are too young")
        return data


class ShopUserProfileEditForm(UserChangeForm):
    class Meta:
        model = ShopUserProfile
        fields = ("gender", "about")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs["class"] = "form-control"
            field.help_text = ""
            if field_name == "password":
                field.widget = HiddenInput()
