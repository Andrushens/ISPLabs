import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from main.forms import SignupForm, CreateReviewForm, UpdateReviewForm
from main.models import Account, Review


User = get_user_model()

@pytest.fixture
def user():
    return User.objects.create_user(username="test", password="123qwe456rty")

@pytest.fixture
def user2():
    return User.objects.create_user(username="test2", password="123qwe456rty")

@pytest.fixture
def account(user):
    return Account.objects.create(user=user)

@pytest.fixture
def review(account):
    return Review.objects.create(title="test", text="test text", author=account)

@pytest.mark.parametrize('param', [
    ('signup'),
    ('login'),
    ('logout'),
    ('create'),
])
def test_render_views(client, param):
    temp_url = reverse(param)
    resp = client.get(temp_url)
    assert resp.status_code == 200 or resp.status_code == 302

@pytest.mark.django_db
def test_register(client):
    data = {"username": "test", "password1": "123qwe456rty", "password2": "123qwe456rty"}
    assert SignupForm(data=data).is_valid()
    client.post("/signup", data)
    assert User.objects.filter(username=data["username"]).count() != 0

@pytest.mark.django_db
def test_login(client, user):
    data = {"username": user.username, "password": "123qwe456rty"}
    client.post("/login", data)
    assert client.post("/login", username=user.username, password="123qwe456rty")
    assert client.login(username=user.username, password="123qwe456rty")

@pytest.mark.django_db
def test_detail_user(client, user):
    resp_get = client.get("/users/{}".format(user.id))
    assert resp_get.status_code == 200

@pytest.mark.django_db
def test_create_review(client, user, account):
    client.login(username=user.username, password="123qwe456rty")
    resp_get = client.get("/qwezxcasd")
    assert resp_get.status_code == 404
    resp_get = client.get("/create")
    assert resp_get.status_code == 200
    data = {"title": "test", "text": "test text"}
    assert CreateReviewForm(data=data).is_valid()
    resp_post = client.post("/create", data)
    assert resp_post.status_code == 302
    assert Review.objects.get(author_id=user.id).author.reviews_created == 1

@pytest.mark.django_db
def test_delete_post(client, user, user2, account, review):
    client.login(username=user2.username, password="123qwe456rty")
    resp_post = client.post("/reviews/" + review.slug + "/delete", {"slug": review.slug})
    assert resp_post.status_code == 302
    client.login(username=user.username, password="123qwe456rty")
    resp_post = client.post("/reviews/" + review.slug + "/delete", {"slug": review.slug})
    assert resp_post.status_code == 302
    assert Review.objects.filter(author=account).first() is None

@pytest.mark.django_db
def test_like_post(client, user, user2, review, account):
    client.login(username=user.username, password="123qwe456rty")
    resp_post = client.post("/reviews/" + review.slug + "/like", {"slug": review.slug})
    assert Review.objects.filter(author=account).first().fans.count() == 0
    client.login(username=user2.username, password="123qwe456rty")
    resp_post = client.post("/reviews/" + review.slug + "/like", {"slug": review.slug})
    assert resp_post.status_code == 302
    assert Review.objects.filter(author=account).first().fans.count() == 1

@pytest.mark.django_db
def test_update_post(client, user, user2, review, account):
    client.login(username=user2.username, password="123qwe456rty")
    client.get("/")
    resp_get = client.get("/reviews/" + review.slug + "/update")
    assert resp_get.status_code == 302
    client.login(username=user.username, password="123qwe456rty")
    resp_get = client.get("/reviews/" + review.slug + "/update")
    assert resp_get.status_code == 200
    data = {"title": "test title 2", "text": "test text"}
    assert UpdateReviewForm(data=data).is_valid()
    resp_post = client.post("/reviews/" + review.slug + "/update", data)
    assert resp_post.status_code == 302
    assert Review.objects.filter(author=account).first().text == data["text"]
    assert Review.objects.count() == 1