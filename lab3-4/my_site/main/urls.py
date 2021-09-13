from django.urls import path
from . import views


urlpatterns = [
    path('', views.home_page, name='home'),
    path('login', views.login_page, name='login'),
    path('signup', views.signup_page, name='signup'),
    path('logout', views.logout_page, name='logout'),
    path('users/<int:pk>', views.UserDetailView.as_view()),
    path('create', views.create_page, name='create'),
    path('reviews/<slug:slug>/update', views.update_page, name='update'),
    path('reviews/<slug:slug>/delete', views.delete_page, name='delete'),
    path('reviews/<slug:slug>/like', views.like_review, name='like'),
    path('reviews/<slug:slug>', views.ReviewsDetailView.as_view()),
]