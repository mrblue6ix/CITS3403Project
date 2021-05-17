![Alt text](app/static/media/logo.png "Title")
# LearnPython Website

# Introduction
LearnPython is an interactive Python tutorial website, where users can learn how to use basic Python and receive feedback on their performance. After Python concepts are introduced, users can immediately run the code in the browser, completing mandatory activities as they progress. 

There are 4 main concepts that are covered:
- Printing in Python
- Numbers and operations
- Strings
- Lists

At the end of these 4 modules, there is a test activity that gives the users a time limit to complete a programming question (FizzBuzz). At the end of the time limit, the user's answer will be submitted and they can view a model solution. 

# Architecture
`LearnPython` is a Flask app using `SQLite` as the backend database, and `SQLAlchemy` as the ORM interface. 

Below is a high-level overview of the file structure within the app:

```bash
.
├── README.md
├── app
│   ├── __init__.py
│   ├── forms.py
│   ├── models.py
│   ├── resources
│   │   ├── 1-printing
│   │   ├── 2-numbers
│   │   ├── 3-strings
│   │   ├── 4-lists
│   │   ├── modules_caleb.yaml
│   │   ├── readme.md
│   │   └── test-1
│   ├── routes.py
│   ├── static
│   │   ├── js
│   │   └── styles
│   └── templates
├── app.db
├── chromedriver.exe
├── config.py
├── docs
├── geckodriver.exe
├── learnpython.py
├── msedgedriver.exe
├── requirements.txt
├── scripts
├── tests
│   ├── functional
│   └── unit
└── unittest.py
```
### Flask front-end logic
Within the `app` folder, which contains the main logic for the `LearnPython` webapp, there are 3 main files:
1. `routes.py`
    - This Flask file handles the routing from one page to the other, and formats our templates depending on dynamic urls and user information.
    - It also handles important security checks such as authentication, error pages, and activity submissions.
2. `forms.py`
    - This file describes the behaviour of the two forms we have in our application, `LoginForm` and `RegistrationForm`. 
    - It ensures that the data entered into our application has appropriate constraints.
3. `models.py`
    - This file is the interface between our application front-end logic and the back-end database. 
    - It outlines the `SQLAlchemy ORM` models that are used to create the database, as well as helper functions which are called by the front-end to modify the database.

- *Attributions*
    - Flask (https://flask.palletsprojects.com/en/2.0.x/)
    - Flask WTForms (https://flask-wtf.readthedocs.io/en/stable)
    - Flask SQLAlchemy (https://flask-sqlalchema. palletsprojects.com/en/2.x/)
    - werkzeug (https://werkzeug.palletsprojects.com/en/2.0.x/)
    - flask_login (https://flask-login.readthedocs.io/en/latest/)


## `Resources` folder
The `resources` folder is where LearnPython developers can easily write new activities and tests and add them to the database. 

Our learning system is separated into `modules` and `activites`, where many `activities` can belong to a single `module`. Modules are overarching concepts in Python, whereas activities target a specific part of that concept. 

The list of modules is created in a `.yaml` file with the following structure:

```yaml
---
1-1-helloworld:
  requires:
  title: Module title goes here
  description: Module description goes here
1-2-printing:
  requires:
    - 1-1-helloworld
  title: Module title goes here
  description: Module description goes here
...
```

Each module can have multiple `requires`, which are modules that must be completed before they are unlocked. This takes the form of a `parent-child` relationship which is reflected in the `ModuleDependency` table of the database. 

Each module in the `.yaml` file has an associated folder with the same name, which contains any number of `activities` which are also `.yaml` files. 

The structure of an activity `.yaml` file is as follows:

```yaml
---
name: 1-1-helloworld
title: Hello, world!
requires: 
prompt: >
  Python is a very simple language that has a very straightforward syntax.
question: >
  Write a line of Python code to print out the the string "`Hello, world!`".
  When you think you are done, press the "Submit" button. 
prefill: print("This line will be printed")
answer: Hello, world!
solution: > 
  Well done! You have completed your first exercise and are officially a programmer!
...
```

Similar to the module structure, each `activity` can depend on none or more other activities, which will be reflected as an `ActivityDependency` parent-child relationship in the database. 

### `scripts` usage to populate database
The `scripts` folder contains a number of helper Python scripts to manually transform the `.yaml` activities and modules into database representations. 

1. `clear-db.py`
- This script allows a developer to clear out specific parts of the database to allow for fast interation.
- Usage is `python3 clear-db.py [app.db]`
- *Attributions*
    - SQLite3 https://docs.python.org/3/library/sqlite3.html
2. `populate-db.py`
- This reads a module file and all the activities within it, then inserts them into a `Sqlite3` database.
- It also reads the relationships between the modules and populates the `Dependency` tables.
- It converts the `markdown` code into valid `html`
- Usage: `python3 populate-db.py [app.db] [app/resources/modules.yaml]`
- *Attributions*
    - SQLite3 https://docs.python.org/3/library/sqlite3.html
    - Python-markdown https://python-markdown.github.io/
3. `add-admin.py`
- This file adds an admin account to the database.
- Usage: `python3 add-admin.py [app.db]`
- *Attributions*
    - SQLite3 https://docs.python.org/3/library/sqlite3.html

## Flask `html` templates
The `templates/` folder contains the `jinja2` `.html` documents that form the basis of our web app. 
- Jinja2 https://jinja.palletsprojects.com/en/3.0.x/
Most templates extend `base.html`, which adds a sidebar and a navigation bar to the app, with the ability to be dynamically formatted depending on the User.

A quick outline of the html templates:
1. `activity.html`
    - This is the webpage shown to users that are completing an activity.
    - It displays some Python content, a question, and an interactive interpreter where users can submit their code. 
    - It also includes an output section where Users can see the `stdout` of their program. 
    - *Attributions*
        - Bootstrap (https://getbootstrap.com/)
        - Skulpt JS libraries (for Python interpreter, https://skulpt.org/using.html)
        - Termynal (https://github.com/ines/termynal)
        - CodeMirror (https://codemirror.net/)
        - Humanize Duration (https://www.npmjs.com/package/humanize-duration)
2. `admin_activity.html`
    - If the user is an administrator, this activity page is shown instead, which displays some basic usage statistics about that activity.
    - *Attributions*
        - Table styling: https://dev.to/dcodeyt/creating-beautiful-html-tables-with-css-428
3. `base.html`
    - This is the base template, which includes a dynamically formatted sidebar and navbar. 
    - *Attributions*
        - Simple Sidebar Bootstrap (https://startbootstrap.com/template/simple-sidebar) 
4. `home.html`
    - This is the landing page for authenticated users.
    - It displays their percentage progress so far in a progress bar
    - It also includes links to all the activites, and shows which activities they can complete and have completed so far. 
5. `login.html`
    - Simply allows a registered User to login
6. `profile.html`
    - Displays the users personal information and some basic statistics
        - Lines of code written
        - Total number of submissions
7. `register.html`
    - Allows a user to create an account on the website
    - Performs some basic checks of input
8. `start_test.html`
    - Landing page for the test start
    - Once the user progresses past this page, the countdown timer will start
9. `tos.html`
    - Terms of service for using this website. 

It also contains very basic `error` pages, as well as the `terms of service`. 

# Launching the Application
Requirements:
- `Flask`
- `python3 -m venv venv`
- `source venv/bin/activate`
- `pip3 install -r requirements.txt`

To launch the application, one needs to ensure that the database is correctly populated with questions.

You can use the scripts above to ensure this is true. In the root directory, execute:

`python3 scripts/populate-db.py app.db app/resources/modules_caleb.yaml`

This will populate the database with activites mentioned in the `modules_caleb.yaml` folder.

The user can then proceed to execute

```bash
flask run
```

In the root directory of the project. 

# Unit tests
There are two types of tests in this webapp
1. Flask front-end and back-end testing
    - These tests are outlined in `test/` folder.
    - The front-end tests navigate over the dashboard to ensure it is working
    - The back-end tests create models and ensure they are populated correctly
    - To run these tests, navigate to the root directory then run
        - `python3 -m pytest`
    - *Attributions*
        - Pytest (https://docs.pytest.org/en/6.2.x/)
2. Selenium user tests
    - `requirements`
        - For each browser to be tested, that browser needs to be installed on the computer, otherwise the test will fail.  
    - These tests are stored in the root directory.
    - The tests are performed on a variety of browsers, including Chrome, Firefox and Edge. The versions of browsers tested on are listed:
        - Chrome:  `90.0.4430.212`
        - Firefox: `88.0.1`
        - Edge:    `90.0.818.62`
    - The webdriver executables for each browser must be stored in the root directory. These executables are required for the specific browser versions listed.
    - To launch the application, follow the steps listed above to launch the flask application. Then, navigate to the root directory and run:
        - `python ut_test_selenium.py`

    - *Attributions*
        - https://www.selenium.dev/
