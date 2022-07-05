from email.policy import default
from django import forms
from .models import Order, OrderItem
from mainapp.models import Product


class OrderItemForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        exclude = ()

    price_for_one = forms.DecimalField(max_digits=2, disabled=True, required=False)
    sum = forms.DecimalField(max_digits=2, disabled=True, required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs["class"] = "form-control"
        self.fields["product"].queryset = Product.objects.filter(
            is_active=True
        ).select_related()
