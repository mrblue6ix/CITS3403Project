import pytest
from app.models import User, Module, Activity

@pytest.fixture(scope="module")
def test_new_user():
    u = User("Caleb", "Cheng", "calebcheng@outlook.com", 
         "caleb1")
    assert u.firstname == "Caleb"
    assert u.lastname == 'Cheng'
    assert u.email == 'calebcheng@outlook.com'
    assert u.username == 'caleb1'
    u.set_password("password1")
    assert u.password != 'password1'
    assert u.is_authenticated
    assert u.is_active
    assert not u.is_anonymous
    assert u.check_password('password1')
    assert not u.is_admin


def test_stats(user):
    loc = user.lines_of_code
    user.add_loc(10)
    assert user.lines_of_code == loc + 10

    total_submissions = user.total_submissions
    user.submit_one()
    assert user.total_submissions == total_submissions + 1
