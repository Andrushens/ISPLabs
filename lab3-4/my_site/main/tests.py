import pytest

from django.test import RequestFactory
from django.contrib.auth.models import User
from .models import *
from .views import *
from django.test import Client


@pytest.fixture
def user(db):
    user = User.objects.create_user(username='testuser', email='', password='password')
    return user


@pytest.mark.django_db
def test_home(user):
    factory = RequestFactory()
    request = factory.get('')
    request.user = user
    response = home_page(request)
    assert response.status_code == 200


@pytest.mark.django_db
def test_login(user):
    factory = RequestFactory()
    request = factory.get('login')
    request.user = user
    response = login_page.as_view()(request)
    assert response.status_code == 200


@pytest.mark.django_db
def test_logout(user):
    factory = RequestFactory()
    request = factory.get('')
    request.user = user
    response = logout_page(request)
    assert response.status_code == 200


@pytest.mark.django_db
def test_create(user):
    factory = RequestFactory()
    request = factory.get('')
    request.user = user
    response = create_page(request)
    assert response.status_code == 200


@pytest.mark.django_db
def test_login_post_view():
    c = Client()
    response = c.post('/login', {'username': 'user', 'password': '123qwe456rty'})
    assert response.status_code == 302


@pytest.mark.parametrize()
def test_signup():
    c = Client()
    response = c.post('/signup', {'username': 'testname', 'password': '123qwe456rty', 
        'confirm_password': '123qwe456rty'})
    assert response.status_code == 302