from django.shortcuts import render
from .models import Setting

context = {"setting": Setting.objects.get(pk=1)}


def index(request):
    settings = Setting.objects.get(pk=1)
    context = {"setting": settings, "page": "home"}
    return render(request, 'index.html', context)


def about(request):
    return render(request, "about.html", context)


def references(request):
    return render(request, "references.html", context)


def contact(request):
    return render(request, "contact.html", context)
