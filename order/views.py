from django.contrib import messages
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from product.models import Category, Product
from .models import Basket, Order, OrderForm, OrderProduct
from django.contrib.auth.decorators import login_required
from home.models import UserProfile
from django.utils.crypto import get_random_string


def index(request):
    category = Category.objects.all()
    basket = Basket.objects.filter(user_id=request.user.id)
    context = {
        "categories": category,
        "baskets": basket,
    }
    return render(request, "shopping_cart.html", context)


@login_required(login_url="/login")
def addtobasket(request, id):
    checkBasket = Basket.objects.filter(product_id=id)
    control = True if checkBasket else False
    data = checkBasket[0] if control else Basket()
    data.user = request.user
    data.product = Product.objects.get(pk=id)
    if request.method == "POST":
        if control:
            data.quantity += int(request.POST["quantity"])
        else:
            data.quantity = int(request.POST["quantity"])
    elif id:
        data.quantity = data.quantity + 1 if control else 1

    amount = Product.objects.get(pk=id).amount
    if data.quantity > amount:
        data.quantity = amount
    data.save()
    request.session["basketCount"] = Basket.objects.filter(
        user_id=request.user.id).count()
    request.session["basketPrice"] = sum(
        [i.amount for i in Basket.objects.filter(user_id=request.user.id)])
    return redirect("order_index")


def deletetobasket(request, id):
    Basket.objects.filter(id=id).delete()
    request.session["basketCount"] = Basket.objects.filter(
        user_id=request.user.id).count()
    request.session["basketPrice"] = sum(
        [i.amount for i in Basket.objects.filter(user_id=request.user.id)])
    return redirect("order_index")


def orderproduct(request):
    category = Category.objects.all()
    current_user = request.user
    shopcart = Basket.objects.filter(user_id=current_user.id)
    total = 0
    for rs in shopcart:
        total += rs.product.price * rs.quantity

    if request.method == 'POST':  # if there is a post
        form = OrderForm(request.POST)
        # return HttpResponse(request.POST.items())
        if form.is_valid():
            # Send Credit card to bank,  If the bank responds ok, continue, if not, show the error
            # ..............

            data = Order()
            # get product quantity from form
            data.first_name = form.cleaned_data['first_name']
            data.last_name = form.cleaned_data['last_name']
            data.address = form.cleaned_data['address']
            data.city = form.cleaned_data['city']
            data.phone = form.cleaned_data['phone']
            data.user = current_user
            data.total = total
            data.ip = request.META.get('REMOTE_ADDR')
            ordercode = get_random_string(5).upper()  # random cod
            data.code = ordercode
            data.save()

            for rs in shopcart:
                detail = OrderProduct()
                detail.order = data  # Order Id
                detail.product = rs.product
                detail.user = current_user
                detail.quantity = rs.quantity
                detail.price = rs.product.price
                detail.amount = rs.amount
                detail.save()
                # ***Reduce quantity of sold product from Amount of Product

                product = Product.objects.get(id=rs.product_id)
                product.amount -= rs.quantity
                product.save()

            # Clear & Delete shopcart
            Basket.objects.filter(user_id=current_user.id).delete()
            request.session['basketCount'] = 0
            messages.add_message(
                request, messages.SUCCESS, "Your Order has been completed. Thank you ")
            return render(request, 'Order_Completed.html', {'ordercode': ordercode, 'categories': category})
        else:
            messages.add_message(request, messages.WARNING, str(form.errors))
            return HttpResponseRedirect("/order/orderproduct")

    form = OrderForm()
    profile = UserProfile.objects.get(user_id=current_user.id)
    context = {
        'shopcart': shopcart,
        'categories': category,
        'total': total,
        'form': form,
        'profile': profile,
    }
    return render(request, 'Order_Form.html', context)


def user_orders(request):
    context = {
        "categories": Category.objects.all(),
        "orders": Order.objects.filter(user_id=request.user.id)
    }
    return render(request, "user_orders.html", context)


def user_orders_details(request, id):
    context = {
        "categories": Category.objects.all(),
        "order": Order.objects.filter(user_id=request.user.id, id=id),
        "order_items": OrderProduct.objects.filter(order_id=id),
    }
    return render(request, "user_order_details.html", context)