from django.urls import path
from . import views


urlpatterns = [
    path('', views.home_page, name='home'),
    path('login', views.login_page, name='login'),
    path('signup', views.signup_page, name='signup'),
    path('logout', views.logout_page, name='logout'),
    path('create', views.create_page, name='create'),
    path("<int:pk>/", views.UserDetailView.as_view()),
    path("<slug:slug>/", views.ReviewsDetailView.as_view()),
]