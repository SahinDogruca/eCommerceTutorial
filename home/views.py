from django.contrib import messages
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from .models import ContactFormMessage, Setting, Comment
from product.models import Product, Category, Image
from django.contrib.auth.models import User
from .forms import *
import json
from django.contrib.auth import logout, login, authenticate
from order.models import Basket


def index(request):
    request.session["basketPrice"] = sum(
        [i.amount for i in Basket.objects.filter(user_id=request.user.id)])
    request.session["basketCount"] = Basket.objects.filter(
        user_id=request.user.id).count()
    settings = Setting.objects.get(pk=1)
    slider = Product.objects.all()[:4]
    category = Category.objects.all()
    deals_of_day_products = Product.objects.all()[:4]
    latest_products = Product.objects.all().order_by("-update_at")
    picked_for_you_products = Product.objects.all().order_by("?")
    context = {
        "setting": settings,
        "page": "home",
        "sliders": slider,
        "categories": category,
        "deals_of_day_products":  deals_of_day_products,
        "latest_products": latest_products,
        "picked_for_you_products": picked_for_you_products,
    }
    return render(request, 'index.html', context)


def about(request):
    settings = Setting.objects.get(pk=1)
    category = Category.objects.all()
    context = {"setting": settings, "categories": category}
    return render(request, "about.html", context)


def references(request):
    settings = Setting.objects.get(pk=1)
    category = Category.objects.all()
    context = {"setting": settings, "categories": category}
    return render(request, "references.html", context)


def contact(request):
    if request.method == "POST":
        data = ContactFormMessage()
        data.name = request.POST["name"]
        data.email = request.POST["email"]
        data.subject = request.POST["subject"]
        data.message = request.POST["message"]
        data.ip = request.META.get("REMOTE_ADDR")
        data.save()
        messages.add_message(request, messages.SUCCESS,
                             "Form Başarıyla Gönderildi.")

    settings = Setting.objects.get(pk=1)
    category = Category.objects.all()
    context = {"setting": settings, "categories": category}
    return render(request, "contact.html", context)


def category_products(request, id, slug):
    products = Product.objects.filter(category_id=id)
    category = Category.objects.all()
    current_category = Category.objects.get(pk=id)
    context = {
        "products": products,
        "categories": category,
        "category": current_category,
    }
    return render(request, "products.html", context)


def product_detail(request, id, slug):
    category = Category.objects.all()
    product = Product.objects.get(pk=id)
    images = Image.objects.filter(product_id=id)
    comment = Comment.objects.filter(product_id=id)
    context = {
        "product": product,
        "images": images,
        "categories": category,
        "comments": comment,
    }
    return render(request, "product_detail.html", context)


def add_comment(request, id):
    url = request.META.get("HTTP_REFERER")
    if request.method == "POST":
        data = Comment()
        data.subject = request.POST["subject"]
        data.comment = request.POST["comment"]
        data.rate = request.POST["rating"]
        data.ip = request.META.get("REMOTE_ADDR")
        data.user = request.user
        data.product = Product.objects.get(pk=id)
        data.status = "New"
        data.save()
        messages.add_message(request, messages.SUCCESS,
                             "Yorum Başarıyla Eklendi.")
        return HttpResponseRedirect(url)
    return HttpResponseRedirect(url)


def search(request):
    if request.method == "POST":
        form = SearchForm(request.POST)
        if form.is_valid():
            category = Category.objects.all()
            query = form.cleaned_data['query']
            catid = form.cleaned_data['catid']

            if catid == 0:
                products = Product.objects.filter(title__icontains=query)
            else:
                products = Product.objects.filter(
                    title__icontains=query, category_id=catid)

            context = {
                "products": products,
                "categories": category,
            }
            return render(request, "product_search.html", context)

    return HttpResponseRedirect("/")


def product_auto_search(request):
    if request.is_ajax():
        q = request.GET.get("term", "")
        product = Product.objects.filter(title__icontains=q)
        result = []
        for rs in product:
            product_json = {}
            product_json = rs.title
            result.append(product_json)
        data = json.dumps(result)
    else:
        data = "fail"
    mimetype = "aplication/json"
    return HttpResponse(data, mimetype)


def logout_view(request):
    logout(request)

    return redirect("index")


def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("index")
        else:
            messages.add_message(request, messages.ERROR,
                                 "KUllanıcı bilgilerini yanlış girdiniz")
            return redirect("login")
    else:
        context = {
            "categories": Category.objects.all()
        }
        return render(request, "login.html", context)


def register_view(request):
    if request.method == "POST":
        first_name = request.POST["first-name"]
        last_name = request.POST["last-name"]
        email = request.POST["email"]
        username = request.POST["username"]
        password = request.POST["password"]
        repassword = request.POST["repassword"]
        if User.objects.filter(email=email).exists():
            messages.add_message(request, messages.ERROR,
                                 "Bu Email daha önce kullanılmış")
            return redirect("register")
        else:
            if User.objects.filter(username=username).exists():
                messages.add_message(
                    request, messages.ERROR, "Bu kullanıcı adı daha önce kullanılmış")
                return redirect("register")
            else:
                if password != repassword:
                    messages.add_message(
                        request, messages.ERROR, "Parolalar Eşleşmiyor")
                    return redirect("register")
                else:
                    user = User.objects.create_user(
                        first_name=first_name, last_name=last_name, email=email, username=username, password=password)
                    user.save()
                    login_user = authenticate(
                        request, username=username, password=password)
                    login(request, login_user)
                    return redirect("index")
    else:
        context = {
            "categories": Category.objects.all()
        }
        return render(request, "register.html", context)
