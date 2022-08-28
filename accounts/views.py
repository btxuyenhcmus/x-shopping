from django.shortcuts import render, redirect
from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required

from accounts.models import Account

from .forms import RegistrationForm


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
