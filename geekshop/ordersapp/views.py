from django.forms import inlineformset_factory
from django.http import HttpResponseBadRequest, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse, reverse_lazy
from ordersapp.models import Order, OrderItem
from ordersapp.forms import OrderItemForm
from django.contrib.auth.decorators import login_required
from utils.mixins import LoginRequiredMixin, TitleMixin
from django.views.generic import ListView, UpdateView
from django.db import transaction

OrderFormSet = inlineformset_factory(Order, OrderItem, form=OrderItemForm, extra=2)


class OrderListView(LoginRequiredMixin, TitleMixin, ListView):
    title = "Orders"
    template_name = "ordersapp/order_list.html"

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).order_by("created_at")


@login_required
@transaction.atomic
def create_order(request):
    basket = request.user.basket
    basket_items = basket.all()
    if not basket_items or not basket.can_create_order():
        return HttpResponseBadRequest()
    order = Order(user=request.user)
    order.save()
    for item in basket_items:
        item = OrderItem(order=order, product=item.product, quantity=item.quantity)
        item.save()
    basket_items.delete()
    return HttpResponseRedirect(reverse("orders:list"))


@login_required
def pay_for_order(request, pk):
    order = get_object_or_404(Order, pk=pk)
    if not order.can_pay:
        return HttpResponseBadRequest()

    order.status = Order.PAID
    order.save()
    return HttpResponseRedirect(reverse("orders:list"))


@login_required
def cancel_order(request, pk):
    order = get_object_or_404(Order, pk=pk)
    if not order.can_cancel:
        return HttpResponseBadRequest()

    order.status = Order.CANCELED
    order.delete()
    return HttpResponseRedirect(reverse("orders:list"))


class OrderUpdateView(LoginRequiredMixin, TitleMixin, UpdateView):
    title = "Edit order"
    template_name = "ordersapp/order_update.html"
    model = Order
    fields = ()

    def get_success_url(self):
        order_id = self.kwargs["pk"]
        return reverse_lazy("orders:update", args=[order_id])

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)

        if self.request.POST:
            data["orderitems"] = OrderFormSet(self.request.POST, instance=self.object)
        else:
            queryset = self.object.order_items.select_related()
            orderitems = OrderFormSet(instance=self.object, queryset=queryset)
            for form in orderitems.forms:
                if form.instance.pk:
                    form.initial["price_for_one"] = form.instance.product.price
                    form.initial["sum"] = (
                        form.instance.product.price * form.initial["quantity"]
                    )
            data["orderitems"] = orderitems
        return data

    def form_valid(self, form):

        context = self.get_context_data()
        orderitems = context["orderitems"]

        with transaction.atomic():
            self.object = form.save()
            if orderitems.is_valid():
                orderitems.instance = self.object
                orderitems.save()

        return super().form_valid(form)
