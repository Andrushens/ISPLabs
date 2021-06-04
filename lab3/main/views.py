from main.models import *
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.generic.base import View
from multiprocessing import Process
import logging

from .forms import CreateReviewForm, SignupForm


logging.basicConfig(filename='logger.log', level=logging.INFO)
log = logging.getLogger(__name__)

@login_required(login_url='login')
def home_page(request):
    reviews = Review.objects.all()
    context = {'reviews': reviews}
    return render(request, 'main/index.html', context)


def signup_page(request):
    if request.user.is_authenticated:
        return redirect('home')

    form = SignupForm()

    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            p = Process(target=log.info, args=("{} just registered".format(form.cleaned_data['username']),))
            p.start()
            p.join()
            form.save()
            return redirect('login')

    context = {'form': form}
    return render(request, 'main/sign-up.html', context)


def login_page(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            p = Process(target=log.info, args=("{} just logged in".format(username),))
            p.start()
            p.join()
            login(request, user)
            return redirect('home')
        
        messages.info(request, 'Incorrect login or password')

    context = {}
    return render(request, 'main/login.html', context)


def logout_page(request):
    p = Process(target=log.info, args=("{} just logged out".format(request.user.username),))
    p.start()
    p.join()
    logout(request)
    return redirect('login')


@login_required(login_url='login')
def create_page(request):
    if request.method == 'POST':
        form = CreateReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.author = request.user
            review.save()
            p = Process(target=log.info, args=("{} just created review {}".format(request.user.username, review.title),))
            p.start()
            p.join()
            return redirect('home')
    form = CreateReviewForm()
    context = {'form': form}
    return render(request, 'main/create.html', context)


class ReviewsDetailView(View):

    def get(self, request, slug):
        review = Review.objects.get(slug=slug)
        context = {"review": review}
        return render(request, 'main/review.html', context)


class UserDetailView(View):

    def get(self, request, pk):
        user = User.objects.get(id=pk)
        reviews = Review.objects.filter(author_id=pk)
        context = {"user": user, "reviews": reviews}
        return render(request, 'main/user.html', context)