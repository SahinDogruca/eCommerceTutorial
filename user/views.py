from django.contrib.auth import update_session_auth_hash
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from product.models import Category
from home.models import UserProfile
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import *


def userProfile(request):
    category = Category.objects.all()
    user_profile = UserProfile.objects.get(user_id=request.user.id)
    context = {
        "categories": category,
        "user_profile": user_profile,
    }
    return render(request, "user_profile.html", context)


def change_password(request):
    if request.method == "POST":
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.add_message(request, messages.SUCCESS,
                                 "Şifreniz başarıyla güncellendi.")
            return redirect("user_profile")
        else:
            messages.error(
                request, 'Please correct the error below.<br>' + str(form.errors))
            return redirect("change_password")
    else:
        form = PasswordChangeForm(request.user)
        return render(request, 'change_password.html', {'form': form, 'categories': Category.objects.all()})


def user_update(request):
    if request.method == 'POST':
        # request.user is user  data
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(
            request.POST, request.FILES, instance=request.user.userprofile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your account has been updated!')
            return redirect("user_profile")
    else:
        category = Category.objects.all()
        user_form = UserUpdateForm(instance=request.user)
        # "userprofile" model -> OneToOneField relatinon with user
        profile_form = ProfileUpdateForm(instance=request.user.userprofile)
        context = {
            'categories': category,
            'user_form': user_form,
            'profile_form': profile_form
        }
        return render(request, 'user_update.html', context)
    return redirect("index")
