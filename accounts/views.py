from django.shortcuts import render, redirect
from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required

from accounts.models import Account
from carts.models import Cart, CartItem
from carts.views import _cart_id

from .forms import RegistrationForm

import requests


def register(request):
    form = RegistrationForm()
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            phone_number = form.cleaned_data['phone_number']
            password = form.cleaned_data['password']
            username = email.split('@')[0]
            user = Account.objects.create_user(
                first_name=first_name, last_name=last_name, email=email, username=username, password=password)
            user.phone_number = phone_number
            user.is_active = True
            user.save()
            messages.success(request=request, message='Register successful!')
            auth.login(request=request, user=user)
            return redirect('dashboard')
        messages.error(request=request, message='Register failed!')
    context = {
        'form': form
    }
    return render(request, 'accounts/register.html', context=context)


def login(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = auth.authenticate(email=email, password=password)
        # If login successful, convert all item cart to user login
        # if not, sent message login failed
        if user is not None:
            try:
                cart = Cart.objects.get(cart_id=_cart_id(request))
                cart_items = CartItem.objects.filter(cart_id=cart)
                for cart_item in cart_items:
                    try:
                        added_cart_item = CartItem.objects.get(
                            product=cart_item.product, user=user)
                        added_cart_item.quantity += cart_item.quantity
                        added_cart_item.save()
                        cart_item.delete()
                    except Exception as e:
                        cart_item.user = user
                        cart_item.save()
            except Exception as e:
                pass
            auth.login(request=request, user=user)
            messages.success(request=request, message="Login successful!")
            url = request.META.get('HTTP_REFERER')
            try:
                query = requests.utils.urlparse(url).query
                params = dict(x.split("=") for x in query.split("&"))
                if "next" in params:
                    next_page = params["next"]
                    return redirect(next_page)
            except Exception:
                pass
            return redirect('dashboard')
        messages.error(request=request, message="Login failed!")
    return render(request, 'accounts/login.html')


@login_required(login_url="login")
def dashboard(request):
    return render(request, 'accounts/dashboard.html')


@login_required(login_url="login")
def logout(request):
    auth.logout(request)
    messages.success(request=request, message="You are logged out!")
    return redirect('login')


def forgotPassword(request):
    return render(request, 'accounts/forgotPassword.html')
