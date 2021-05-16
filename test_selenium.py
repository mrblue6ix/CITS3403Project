import os
import random, string
from app import app, db
from time import sleep
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

def test_selenium_chrome():
    st = seleniumTest()
    try:
        # Initiate Chrome browser
        driver = st.setUp(0)
        print("Webdriver setup - OK")
    except:
        print("Failure - webdriver setup failed")
        return None

    # Open website and create a new account
    try:
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
        # Once account is created, assert true if on homepage
        assert driver.title == "Learn Python - Homepage"
        print("Account creation - OK")
    except:
        print("Failure - account creation failed")
        return None

    # Navigate to profile page, and assert account details are stored correctly
    try:
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
        print("Profile page - OK")
    except:
        print("Failure - account details stored incorrectly")
        return None

    # Go to locked activity and assert activity is locked
    try:
        driver.get("http://127.0.0.1:5000/learn/1-printing/1-2-variables")
        lockMessage = driver.find_element_by_id("lockmessage").text
        assert lockMessage == "🔒 This content is locked! 🔒"
        print("Locked activities - OK")
    except:
        print("Failure - locked activity is unlocked, inaccessible or doesn't exist")
        return None

    # Go to unlocked activity and assert activity is unlocked
    try:
        driver.get("http://127.0.0.1:5000/learn/1-printing/1-1-helloworld")
        pageactivity = driver.find_element_by_id("pageactivity").text
        assert pageactivity == "Hello, world!"
        print("Unlocked activities - OK")
    except:
        print("Failure - unlocked activity is locked, inaccessible or doesn't exist")
        return None

    # Check prefill is correctly displayed, and the run function outputs the written code
    try:
        prefill = driver.find_element_by_id("yourcode")
        assert prefill.get_attribute("value") == 'print("This line will be printed")'
        driver.find_element_by_id("run").click()
        output = driver.find_element_by_id("output")
        assert output.text == "This line will be printed"
        print("Activity prefill - OK")
    except:
        print("Failure - activity prefill is incorrect")
        return None

    # Attempt to submit correct answer
    try:
        code = driver.find_element_by_css_selector(".CodeMirror")
        driver.execute_script('arguments[0].CodeMirror.setValue(arguments[1])', code, 'print("Hello, world!")')
        driver.find_element_by_id("save").click()
        driver.find_element_by_id("run").click()
        output = driver.find_element_by_id("output")
        assert output.text == "Hello, world!"
        driver.get("http://127.0.0.1:5000/learn/1-printing/1-1-helloworld")
        prefill = driver.find_element_by_id("yourcode")
        assert prefill.get_attribute("value") == 'print("Hello, world!")'
        driver.find_element_by_id("submit").click()
        sleep(1) # Pause to let javascript run
        
    except:
        print("Failure - Couldn't submit answer")
        return None
    
    # Check user statistics are updated correctly
    try:
        driver.get("http://127.0.0.1:5000/profile")
        recordedLines = driver.find_element_by_id("lines").text
        assert recordedLines == "Total lines of code submitted: 1"
        recordedSubmissions = driver.find_element_by_id("submissions").text
        assert recordedSubmissions == "Total number of submissions: 1"
        print("Account statistics - OK")
    except:
        print("Failure - User statistics failed to update")
        return None
    print("All OK for Chrome!")


def test_selenium_firefox():
    st = seleniumTest()

    try:
        # Initiate Firefox browser
        driver = st.setUp(0)
        print("Webdriver setup - OK")
    except:
        print("Failure - webdriver setup failed")
        return None

    # Open website and create a new account
    try:
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
        # Once account is created, assert true if on homepage
        assert driver.title == "Learn Python - Homepage"
        print("Account creation - OK")
    except:
        print("Failure - account creation failed")
        return None

    # Navigate to profile page, and assert account details are stored correctly
    try:
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
        print("Profile page - OK")
    except:
        print("Failure - account details stored incorrectly")
        return None

    # Go to locked activity and assert activity is locked
    try:
        driver.get("http://127.0.0.1:5000/learn/1-printing/1-2-variables")
        lockMessage = driver.find_element_by_id("lockmessage").text
        assert lockMessage == "🔒 This content is locked! 🔒"
        print("Locked activities - OK")
    except:
        print("Failure - locked activity is unlocked, inaccessible or doesn't exist")
        return None

    # Go to unlocked activity and assert activity is unlocked
    try:
        driver.get("http://127.0.0.1:5000/learn/1-printing/1-1-helloworld")
        pageactivity = driver.find_element_by_id("pageactivity").text
        assert pageactivity == "Hello, world!"
        print("Unlocked activities - OK")
    except:
        print("Failure - unlocked activity is locked, inaccessible or doesn't exist")
        return None

    # Check prefill is correctly displayed, and the run function outputs the written code
    try:
        prefill = driver.find_element_by_id("yourcode")
        assert prefill.get_attribute("value") == 'print("This line will be printed")'
        driver.find_element_by_id("run").click()
        output = driver.find_element_by_id("output")
        assert output.text == "This line will be printed"
        print("Activity prefill - OK")
    except:
        print("Failure - activity prefill is incorrect")
        return None

    # Attempt to submit correct answer
    try:
        code = driver.find_element_by_css_selector(".CodeMirror")
        driver.execute_script('arguments[0].CodeMirror.setValue(arguments[1])', code, 'print("Hello, world!")')
        driver.find_element_by_id("save").click()
        driver.find_element_by_id("run").click()
        output = driver.find_element_by_id("output")
        assert output.text == "Hello, world!"
        driver.get("http://127.0.0.1:5000/learn/1-printing/1-1-helloworld")
        prefill = driver.find_element_by_id("yourcode")
        assert prefill.get_attribute("value") == 'print("Hello, world!")'
        driver.find_element_by_id("submit").click()
        sleep(1) # Pause to let javascript run
        
    except:
        print("Failure - Couldn't submit answer")
        return None
    
    # Check user statistics are updated correctly
    try:
        driver.get("http://127.0.0.1:5000/profile")
        recordedLines = driver.find_element_by_id("lines").text
        assert recordedLines == "Total lines of code submitted: 1"
        recordedSubmissions = driver.find_element_by_id("submissions").text
        assert recordedSubmissions == "Total number of submissions: 1"
        print("Account statistics - OK")
    except:
        print("Failure - User statistics failed to update")
        return None
    print("All OK for Firefox!")
    
def test_selenium_edge():
    st = seleniumTest()

    # Initiate Edge browser
    try:
        driver = st.setUp(0)
        print("Webdriver setup - OK")
    except:
        print("Failure - webdriver setup failed")
        return None

    # Open website and create a new account
    try:
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
        # Once account is created, assert true if on homepage
        assert driver.title == "Learn Python - Homepage"
        print("Account creation - OK")
    except:
        print("Failure - account creation failed")
        return None

    # Navigate to profile page, and assert account details are stored correctly
    try:
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
        print("Profile page - OK")
    except:
        print("Failure - account details stored incorrectly")
        return None

    # Go to locked activity and assert activity is locked
    try:
        driver.get("http://127.0.0.1:5000/learn/1-printing/1-2-variables")
        lockMessage = driver.find_element_by_id("lockmessage").text
        assert lockMessage == "🔒 This content is locked! 🔒"
        print("Locked activities - OK")
    except:
        print("Failure - locked activity is unlocked, inaccessible or doesn't exist")
        return None

    # Go to unlocked activity and assert activity is unlocked
    try:
        driver.get("http://127.0.0.1:5000/learn/1-printing/1-1-helloworld")
        pageactivity = driver.find_element_by_id("pageactivity").text
        assert pageactivity == "Hello, world!"
        print("Unlocked activities - OK")
    except:
        print("Failure - unlocked activity is locked, inaccessible or doesn't exist")
        return None

    # Check prefill is correctly displayed, and the run function outputs the written code
    try:
        prefill = driver.find_element_by_id("yourcode")
        assert prefill.get_attribute("value") == 'print("This line will be printed")'
        driver.find_element_by_id("run").click()
        output = driver.find_element_by_id("output")
        assert output.text == "This line will be printed"
        print("Activity prefill - OK")
    except:
        print("Failure - activity prefill is incorrect")
        return None

    # Attempt to submit correct answer
    try:
        code = driver.find_element_by_css_selector(".CodeMirror")
        driver.execute_script('arguments[0].CodeMirror.setValue(arguments[1])', code, 'print("Hello, world!")')
        driver.find_element_by_id("save").click()
        driver.find_element_by_id("run").click()
        output = driver.find_element_by_id("output")
        assert output.text == "Hello, world!"
        driver.get("http://127.0.0.1:5000/learn/1-printing/1-1-helloworld")
        prefill = driver.find_element_by_id("yourcode")
        assert prefill.get_attribute("value") == 'print("Hello, world!")'
        driver.find_element_by_id("submit").click()
        sleep(1) # Pause to let javascript run
        
    except:
        print("Failure - Couldn't submit answer")
        return None
    
    # Check user statistics are updated correctly
    try:
        driver.get("http://127.0.0.1:5000/profile")
        recordedLines = driver.find_element_by_id("lines").text
        assert recordedLines == "Total lines of code submitted: 1"
        recordedSubmissions = driver.find_element_by_id("submissions").text
        assert recordedSubmissions == "Total number of submissions: 1"
        print("Account statistics - OK")
    except:
        print("Failure - User statistics failed to update")
        return None
    print("All OK for Edge!")

# Perform the tests on each browser
print("Test Chrome implementation:")
test_selenium_chrome()
print()
print("Test Firefox implementation:")
test_selenium_firefox()
print()
print("Test Edge implementation:")
test_selenium_edge()