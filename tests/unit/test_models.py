import pytest
from app.models import User, Module, Activity

# Tests follow the GIVEN WHEN THEN structure

def test_new_user():
    # GIVEN the user model 
    # WHEN a new user is created
    # THEN check the fields are populated correctly
    # and password hashing works
    u = User(firstname="Caleb", lastname="Cheng", email="calebcheng@outlook.com", 
         username="caleb1")
    assert u.firstname == "Caleb"
    assert u.lastname == 'Cheng'
    assert u.email == 'calebcheng@outlook.com'
    assert u.username == 'caleb1'
    u.set_password("password1")
    assert u.password_hash != 'password1'
    assert u.is_authenticated
    assert u.is_active
    assert not u.is_anonymous
    assert u.check_password('password1')
    assert not u.is_admin

def test_new_activity():
    # GIVEN the activity model
    # WHEN a new activity is created 
    # THEN check that the fields are populated correctly 
    a = Activity(name='1-1-helloworld', title='Hello, world!',
                prompt='This is a hello world activity')
    assert a.name == '1-1-helloworld'
    assert a.title == 'Hello, world!'
    assert a.prompt == 'This is a hello world activity'

# both user and activity will be added to the
# global testing context
@pytest.fixture(scope='module')
def new_user():
    user = User(firstname='John', lastname='Smith',
            email='jsmith@gmail.com', username='jsmith')
    return user

@pytest.fixture(scope='module')
def new_activity():
    a = Activity(name='1-1-helloworld', title='Hello, world!',
                prompt='This is a hello world activity')
    return a

def test_make_user_activity(new_user, new_activity):
    # GIVEN a user and an activity
    # WHEN a new userActivity is created
    # THEN the fields should be populated and methods callable
    ua = new_activity.makeUserActivity(new_user)
    assert ua.user_id == new_user.id
    assert ua.activity_id == new_activity.id

    # Try setting the saved code section
    ua.save_code('print("Hello, world!")')
    assert ua.saved == 'print("Hello, world!")'

    # Try setting the user activity as completed
    ua.set_completion(1)
    assert ua.is_completed == 1


def test_stats(new_user):
    assert new_user.lines_of_code == 0
    loc = new_user.lines_of_code
    new_user.add_loc(10)
    assert new_user.lines_of_code == loc + 10

    total_submissions = new_user.total_submissions
    new_user.submit_one()
    assert new_user.total_submissions == total_submissions + 1
