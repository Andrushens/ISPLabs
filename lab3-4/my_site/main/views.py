from django.http.response import Http404
from .models import *
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.generic.base import View
from .forms import CreateReviewForm, SignupForm, UpdateReviewForm

from threading import Thread
import logging
import configparser


config = configparser.ConfigParser()
config.read('cnf.ini')
logging.basicConfig(
    level=config['LOGGING']['level'],
    filename=config['LOGGING']['filename']
)
log = logging.getLogger(__name__)


def home_page(request):
    reviews = Review.objects.select_related('author')
    context = {'liked_reviews': reviews[:3], 'reviews': reviews}
    return render(request, 'main/index.html', context)


def signup_page(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            p = Thread(target=log.info, args=("{} registered".format(form.cleaned_data['username']),))
            p.start()
            form.save()
            return redirect('login')
        messages.error(request, 'Incorrect login or password')

    form = SignupForm()
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
            if (Account.objects.filter(user=user)).count() == 0:
                Account.objects.create(user=user)
            p = Thread(target=log.info, args=("{} logged in".format(username),))
            p.start()
            login(request, user)
            return redirect('home')
        messages.error(request, 'Incorrect login or password')
    return render(request, 'main/login.html', {})


def logout_page(request):
    p = Thread(target=log.info, args=("{} logged out".format(request.user.username),))
    p.start()
    logout(request)
    return redirect('login')


@login_required(login_url='login')
def create_page(request):
    if request.method == 'POST':
        form = CreateReviewForm(request.POST)
        if form.is_valid() and Review.objects.filter(title=request.POST['title']).count() == 0:
            review = form.save(commit=False)
            review.author = Account.objects.filter(user_id=request.user.id).first()
            review.author.reviews_created += 1
            review.author.save()
            review.save()
            p = Thread(target=log.info, args=("{} created review {}".format(request.user.username, review.title),))
            p.start()
            return redirect('home')
        if Review.objects.filter(title=request.POST['title']).count() == 1:
            messages.error(request, 'Review {} already exists'.format(request.POST['title']))
        else:   
            messages.error(request, 'Incorrect Input')
        p = Thread(target=log.error, args=("{} caused error on creating review".format(request.user.username),))
        p.start()

    form = CreateReviewForm()
    context = {'form': form}
    return render(request, 'main/create.html', context)


@login_required(login_url='login')
def delete_page(request, slug):
    if request.user != Review.objects.filter(slug=slug).first().author.user:
        return redirect(request.path[:-7])
    review = Review.objects.filter(slug=slug).get()
    review.author.reviews_created -= 1
    review.author.save()
    review.delete()
    p = Thread(target=log.info, args=("{} deleted review {}".format(request.user.username, slug),))
    p.start()
    return redirect('home')


@login_required(login_url='login')
def update_page(request, slug):
    if request.user != Review.objects.filter(slug=slug).first().author.user:
        return redirect(request.path[:-7])

    review = Review.objects.filter(slug=slug).get()
    if request.method == 'POST':
        form = UpdateReviewForm(request.POST, instance=review)
        if form.is_valid() and Review.objects.filter(title=request.POST['title']).count() == 0:
            review = form.save(commit=False)
            review.save()
            p = Thread(target=log.info, args=("{} edited review {}".format(request.user.username, review.title),))
            p.start()
            return redirect('home')
        if Review.objects.filter(title=request.POST['title']).count() == 1:
            messages.error(request, 'Review {} already exists'.format(request.POST['title']))
        else:   
            messages.error(request, 'Incorrect Input')
        p = Thread(target=log.error, args=("{} caused error on updating review".format(request.user.username),))
        p.start()

    context = {'review': review}
    return render(request, 'main/update.html', context)


@login_required(login_url='login')
def like_review(request, slug):
    if request.user == Review.objects.filter(slug=slug).first().author.user:
        return redirect(request.path[:-5])

    review = Review.objects.get(slug=slug)
    if review.fans.filter(username=request.user.username).count() == 0:
        review.fans.add(request.user)
        review.likes += 1
        p = Thread(target=log.info, args=("{} liked review {}".format(request.user.username, slug),))
    else:
        review.fans.remove(request.user)
        review.likes -= 1
        p = Thread(target=log.info, args=("{} disliked review {}".format(request.user.username, slug),))
    review.save()
    p.start()

    return redirect(request.path[:-5])


class ReviewsDetailView(View):

    def get(self, request, slug):
        try:
            review = Review.objects.get(slug=slug)
            context = {"review": review}
            return render(request, 'main/review.html', context)
        except:
            raise Http404


class UserDetailView(View):

    def get(self, request, pk):
        try:
            reviews = Review.objects.select_related('author').filter(author_id=pk)
            context = {"reviews": reviews}
            Account.objects.get(user_id=pk)
            return render(request, 'main/user.html', context)
        except:
            raise Http404