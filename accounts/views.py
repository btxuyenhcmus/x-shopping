from django.shortcuts import render, redirect
from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required

from accounts.models import Account

from .forms import RegistrationForm


def register(request): 
    form = RegistrationForm()
    context = {
        'form': form
    }
    return render(request, 'accounts/register.html', context=context)


def login(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = auth.authenticate(email=email, password=password)
        if not user:
            messages.error(request=request, message="Login failed!")
        else:
            auth.login(request=request, user=user)
            messages.success(request=request, message="Login successful!")
            return redirect('dashboard')
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
