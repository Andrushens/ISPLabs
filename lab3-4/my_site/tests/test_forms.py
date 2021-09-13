import pytest

from main.forms import UpdateReviewForm, CreateReviewForm, SignupForm


@pytest.fixture
def user_data():
    return {"username": "test", "password1": "123qwe456rty", "password2": "123qwe456rty"}

@pytest.fixture
def review_data():
    return {"title": "title123", "text": "some text"}

@pytest.fixture
def incorrect_review_data():
    return {"title": "", "text": "some text"}

@pytest.fixture
def incorrect_title_review_data():
    return {"title": "title-123", "text": "some text"}

@pytest.mark.django_db
def test_user_reg(user_data):
    assert SignupForm(data=user_data).is_valid()

@pytest.mark.django_db
def test_review_create(review_data, incorrect_title_review_data, incorrect_review_data):
    assert CreateReviewForm(data=review_data).is_valid()
    assert not CreateReviewForm(data=incorrect_review_data).is_valid()
    assert not CreateReviewForm(data=incorrect_title_review_data).is_valid()

@pytest.mark.django_db
def test_review_update(review_data, incorrect_title_review_data, incorrect_review_data):
    assert UpdateReviewForm(data=review_data).is_valid()
    assert not UpdateReviewForm(data=incorrect_review_data).is_valid()
