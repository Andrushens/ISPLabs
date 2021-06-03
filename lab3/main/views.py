from main.models import User
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .forms import SignupForm


@login_required(login_url='login')
def homePage(request):
    return render(request, 'main/index.html')


def signupPage(request):
    if request.user.is_authenticated:
        return redirect('home')

    form = SignupForm()

    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account successfully created')
            return redirect('login')

    context = {'form': form}
    return render(request, 'main/sign-up.html', context)


def loginPage(request):
    if request.user.is_authenticated:
        return redirect('home')
        
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        
        messages.info(request, 'Incorrect login or password')

    context = {}
    return render(request, 'main/login.html', context)


def logoutPage(request):
    logout(request)
    return redirect('login')
