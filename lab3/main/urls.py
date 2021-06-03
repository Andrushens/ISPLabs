from django.urls import path
from . import views


urlpatterns = [
    path('', views.homePage, name='home'),
    path('login', views.loginPage, name='login'),
    path('signup', views.signupPage, name='sign-up'),
    path('logout', views.logoutPage, name='logout'),
]