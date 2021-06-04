from django.urls import reverse
from django.contrib.auth import User
import pytest
from django.test import Client, RequestFactory
from .views import *
from .forms import *


@pytest.mark.parametrize('param', [
    'products:home',
    'login',
    'register'
])
@pytest.mark.django_db
def test_views(client, param):
    url = reverse(param)
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_get_product_view(product_data, client):
    url = product_data.get_absolute_url()
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_get_category_view(category_data, client):
    url = category_data.get_absolute_url()
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_login_form_valid(user_data, db):
    form_data = {'email': user_data.email, 'password': user_data.password}
    form = SignInForm(data=form_data)
    assert form.is_valid() is True


@pytest.mark.django_db
def test_login_post_view(user_data, db):
    c = Client()
    login_url = reverse('login')
    response = c.post(login_url, {'email': 'test@gmail.com', 'password': 'test_password'})
    assert response.status_code == 302


@pytest.mark.django_db
def test_get_profile_view(user_profile_data, client):
    factory = RequestFactory()
    request = factory.get('')
    request.user = user_profile_data.user
    view = ProfileView()
    response = view.get(request)
    assert response.status_code == 200


@pytest.mark.django_db
def test_get_cart_view(user_cart_data, client):
    factory = RequestFactory()
    request = factory.get('')
    request.user = user_cart_data
    view = CartView()
    response = view.get(request)
    assert response.status_code == 200


@pytest.mark.django_db
def test_add_to_cart(user_cart_data, product_data):
    kwargs = {'slug': product_data.slug}
    url = reverse('add_to_cart', kwargs=kwargs)
    factory = RequestFactory()
    request = factory.get(url)
    request.user = user_cart_data
    response = AddToCartView.as_view()(request, **kwargs)
    assert response.status_code == 302


@pytest.mark.django_db
def test_delete_from_cart(user_cart_data, product_data):
    kwargs = {'slug': product_data.slug}
    url = reverse('add_to_cart', kwargs=kwargs)
    factory = RequestFactory()
    request = factory.get(url)
    request.user = user_cart_data
    AddToCartView.as_view()(request, **kwargs)
    url = reverse('delete_from_cart', kwargs=kwargs)
    request = factory.get(url)
    request.user = user_cart_data
    response = DeleteFromCartView.as_view()(request, **kwargs)
    assert response.status_code == 302