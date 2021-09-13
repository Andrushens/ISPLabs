import pytest
from main.models import Account, Review
from django.contrib.auth.models import User


@pytest.fixture
def user():
    return User.objects.create_user(username="test", password="123qwe456rty")

@pytest.fixture
def account(user):
    return Account.objects.create(user=user)

@pytest.fixture
def review(account):
    return Review.objects.create(author=account, title="Title", text="some text")

@pytest.mark.django_db
def test_review(review, account):
    assert Review.objects.count() == 1
    assert Review.objects.first().author == account 
    assert Review.objects.first().fans.count() == 0 
    assert str(Review.objects.first()) == Review.objects.first().title

@pytest.mark.django_db
def test_user(review):
    assert User.objects.count() == 1

@pytest.mark.django_db
def test_account(account):
    assert Account.objects.count() == 1