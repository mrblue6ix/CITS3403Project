import os
import random, string
from app import app, db
from app.models import User, Activity, Module, UserActivity, ActivityDependency, ModuleDependency
from selenium import webdriver
from msedge.selenium_tools import Edge, EdgeOptions

class seleniumTest:
    def setUp(self, num):
        basedir = os.path.abspath(os.path.dirname(__file__))
        self.app = app.test_client()
        app.config['SQLALCHEMY_DATABASE_URI'] = \
            'sqlite:///'+os.path.join(basedir,'app.db')
        if num == 0:
            options = webdriver.ChromeOptions()
            options.add_experimental_option('excludeSwitches', ['enable-logging'])
            self.driver = webdriver.Chrome(options=options)
        elif num == 1:
            self.driver = webdriver.Firefox()
        else:
            options = EdgeOptions()
            options.use_chromium = True
            options.add_experimental_option('excludeSwitches', ['enable-logging'])
            self.driver = Edge(options=options)
        return self.driver
    
    def tearDown(self):
        db.session.rollback()

def test_new_user():
# GIVEN the user model 
# WHEN a new user is created
# THEN check the fields are populated correctly
# and password hashing works
    try:
        u = User(firstname="testFirstname", lastname="testLastname", email="testEmail", 
                 username="testUsername")
        assert u.firstname == "testFirstname"
        assert u.lastname == "testLastname"
        assert u.email == "testEmail"
        assert u.username == "testUsername"
        u.set_password("testPassword")
        assert u.password_hash != 'testPassword'
        assert u.is_authenticated
        assert u.is_active
        assert not u.is_anonymous
        assert u.check_password('testPassword')
        assert not u.is_admin
        return "Ok"
    except Exception:
        return "Failed"
    
def test_new_activity():
# GIVEN the activity model
# WHEN a new activity is created 
# THEN check that the fields are populated correctly 
    try:
        a = Activity(id=25, name='testName', prompt='testPrompt', answer='testAnswer', title='testTitle', solution='testSolution')
        assert a.id == 25
        assert a.name == 'testName'
        assert a.prompt == 'testPrompt'
        assert a.answer == 'testAnswer'
        assert a.title == 'testTitle'
        assert a.solution == 'testSolution'
        return "Ok"
    except Exception:
        return "Failed"
        

def test_new_module():
# GIVEN the module model
# WHEN a new module is created
# THEN check that the fields are populated correctly
    try:
        m = Module(id=25, title='testTitle', description='testDescription', name='testName')
        assert m.id == 25
        assert m.title == 'testTitle'
        assert m.description == 'testDescription'
        assert m.name == 'testName'
        return "Ok"
    except Exception:
        return "Failed"
        
    
def test_new_user_activity():
# GIVEN the user activity model
# WHEN new user activity is created
# THEN check that the fields are populated correctly
    try:
        ua = UserActivity(user_activity_id=3, user_id=12, activity_id=30)
        assert ua.user_activity_id == 3
        assert ua.user_id == 12
        assert ua.activity_id == 30
        return "Ok"
    except:
        return "Failure"
    
def test_new_activity_dependency():
# GIVEN the activity dependency model
# WHEN a new activity is created
# THEN check that the fields are populated correctly
    try:
        ad = ActivityDependency(id=1, parent=3, child=4)
        assert ad.id == 1
        assert ad.parent == 3
        assert ad.child == 4
        return "Ok"
    except:
        return "Failure"
        
    
def test_new_module_dependency():
# GIVEN the module dependency model
# WHEN a new module is created
# THEN check that the fields are populated correctly
    try:
        md = ModuleDependency(id=1, parent=2, child=3)
        assert md.id == 1
        assert md.parent == 2
        assert md.child == 3
        return "Ok"
    except:
        return "Failure"
        

def test_selenium_chrome():
    st = seleniumTest()
    try:
        driver = st.setUp(0)
        driver.get("http://127.0.0.1:5000/")
        username = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(25))
        email = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(35))
        driver.find_element_by_link_text("Register").click()
        driver.find_element_by_id("username").send_keys(username)
        driver.find_element_by_id("firstname").send_keys("Chrome")
        driver.find_element_by_id("lastname").send_keys("Test")
        driver.find_element_by_id("email").send_keys(email)
        driver.find_element_by_id("password").send_keys("chromePassword")
        driver.find_element_by_id("confirm").send_keys("chromePassword")
        driver.find_element_by_id("accept_tos").click()
        driver.find_element_by_id("submit").click()
        driver.find_element_by_id("username").send_keys(username)
        driver.find_element_by_id("password").send_keys("chromePassword")
        driver.find_element_by_id("submit").click()
        assert driver.title == "Learn Python - Homepage"
        driver.get("http://127.0.0.1:5000/profile")
        assert driver.title == "Learn Python - Profile"
        recordedUsername = driver.find_element_by_id("username").text
        assert recordedUsername == "Username: " + username
        recordedEmail = driver.find_element_by_id("email").text
        assert recordedEmail == "Email: " + email
        recordedLines = driver.find_element_by_id("lines").text
        assert recordedLines == "Total lines of code submitted: 0"
        recordedSubmissions = driver.find_element_by_id("submissions").text
        assert recordedSubmissions == "Total number of submissions: 0"
        driver.get("http://127.0.0.1:5000/learn/1-printing/1-2-variables")
        lockMessage = driver.find_element_by_id("lockmessage").text
        assert lockMessage == "🔒 This content is locked! 🔒"
        driver.get("http://127.0.0.1:5000/learn/1-printing/1-1-helloworld")
        assert driver.title == "Learn Python - Question"
        prefill = driver.find_element_by_id("yourcode")
        assert prefill.get_attribute("value") == 'print("This line will be printed")'
        driver.find_element_by_id("run").click()
        output = driver.find_element_by_id("output").text
        assert output == "This line will be printed"

        #driver.find_element_by_id("submit").click()
        #driver.get("http://127.0.0.1:5000/profile")
        #recordedLines = driver.find_element_by_id("lines").text
        #assert recordedLines == "Total lines of code submitted: 1"
        #recordedSubmissions = driver.find_element_by_id("submissions").text
        #assert recordedSubmissions == "Total number of submissions: 1"

        st.tearDown()
        return "Ok"
    except Exception:
        return "Failed"

def test_selenium_firefox():
    st = seleniumTest()
    try:
        driver = st.setUp(1)
        driver.get("http://127.0.0.1:5000/")
        username = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(25))
        email = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(35))
        driver.find_element_by_link_text("Register").click()
        driver.find_element_by_id("username").send_keys(username)
        driver.find_element_by_id("firstname").send_keys("Firefox")
        driver.find_element_by_id("lastname").send_keys("Test")
        driver.find_element_by_id("email").send_keys(email)
        driver.find_element_by_id("password").send_keys("firefoxPassword")
        driver.find_element_by_id("confirm").send_keys("firefoxPassword")
        driver.find_element_by_id("accept_tos").click()
        driver.find_element_by_id("submit").click()
        driver.find_element_by_id("username").send_keys(username)
        driver.find_element_by_id("password").send_keys("firefoxPassword")
        driver.find_element_by_id("submit").click()
        assert driver.title == "Learn Python - Homepage"
        driver.get("http://127.0.0.1:5000/profile")
        assert driver.title == "Learn Python - Profile"
        recordedUsername = driver.find_element_by_id("username").text
        assert recordedUsername == "Username: " + username
        recordedEmail = driver.find_element_by_id("email").text
        assert recordedEmail == "Email: " + email
        recordedLines = driver.find_element_by_id("lines").text
        assert recordedLines == "Total lines of code submitted: 0"
        recordedSubmissions = driver.find_element_by_id("submissions").text
        assert recordedSubmissions == "Total number of submissions: 0"
        driver.get("http://127.0.0.1:5000/learn/1-printing/1-2-variables")
        lockMessage = driver.find_element_by_id("lockmessage").text
        assert lockMessage == "🔒 This content is locked! 🔒"
        driver.get("http://127.0.0.1:5000/learn/1-printing/1-1-helloworld")
        assert driver.title == "Learn Python - Question"
        prefill = driver.find_element_by_id("yourcode")
        assert prefill.get_attribute("value") == 'print("This line will be printed")'
        driver.find_element_by_id("run").click()
        output = driver.find_element_by_id("output").text
        assert output == "This line will be printed"
        st.tearDown()
        return "Ok"
    except Exception:
        return "Failed"
    
def test_selenium_edge():
    st = seleniumTest()
    try:
        driver = st.setUp(2)
        driver.get("http://127.0.0.1:5000/")
        username = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(25))
        email = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(35))
        driver.find_element_by_link_text("Register").click()
        driver.find_element_by_id("username").send_keys(username)
        driver.find_element_by_id("firstname").send_keys("Edge")
        driver.find_element_by_id("lastname").send_keys("Test")
        driver.find_element_by_id("email").send_keys(email)
        driver.find_element_by_id("password").send_keys("edgePassword")
        driver.find_element_by_id("confirm").send_keys("edgePassword")
        driver.find_element_by_id("accept_tos").click()
        driver.find_element_by_id("submit").click()
        driver.find_element_by_id("username").send_keys(username)
        driver.find_element_by_id("password").send_keys("edgePassword")
        driver.find_element_by_id("submit").click()
        assert driver.title == "Learn Python - Homepage"
        driver.get("http://127.0.0.1:5000/profile")
        assert driver.title == "Learn Python - Profile"
        recordedUsername = driver.find_element_by_id("username").text
        assert recordedUsername == "Username: " + username
        recordedEmail = driver.find_element_by_id("email").text
        assert recordedEmail == "Email: " + email
        recordedLines = driver.find_element_by_id("lines").text
        assert recordedLines == "Total lines of code submitted: 0"
        recordedSubmissions = driver.find_element_by_id("submissions").text
        assert recordedSubmissions == "Total number of submissions: 0"
        driver.get("http://127.0.0.1:5000/learn/1-printing/1-2-variables")
        lockMessage = driver.find_element_by_id("lockmessage").text
        assert lockMessage == "🔒 This content is locked! 🔒"
        driver.get("http://127.0.0.1:5000/learn/1-printing/1-1-helloworld")
        assert driver.title == "Learn Python - Question"
        prefill = driver.find_element_by_id("yourcode")
        assert prefill.get_attribute("value") == 'print("This line will be printed")'
        driver.find_element_by_id("run").click()
        output = driver.find_element_by_id("output").text
        assert output == "This line will be printed"
        st.tearDown()
        return "Ok"
    except Exception:
        return "Failed"

# Perform the tests
print("Test new user: " + str(test_new_user()))
print("Test new activity: " + str(test_new_activity()))
print("Test new module: " + str(test_new_module()))
print("Test new user activity: " + str(test_new_user_activity()))
print("Test new activity dependency: " + str(test_new_activity_dependency()))
print("Test new module dependency: " + str(test_new_module_dependency()))
print("Test Chrome implementation: " + str(test_selenium_chrome()))
print("Test Firefox implementation: " + str(test_selenium_firefox()))
print("Test Edge implementation: " + str(test_selenium_edge()))