import sqlite3
import sys
from werkzeug.security import generate_password_hash, check_password_hash

args = sys.argv
if len(args) < 2:
    print("Incorrect num of args use script.py [app.db]")
conn = sqlite3.connect(args[1])
cursor = conn.cursor()

cursor.execute("INSERT INTO User(firstname, lastname, email, username, password_hash, is_admin) VALUES (?,?,?,?,?,?)",
                ("admini", "strator", "admin@learnpython.com", "admin", generate_password_hash("admin"), 1))
print("Added administrator account with credentials admin/admin")
conn.commit()