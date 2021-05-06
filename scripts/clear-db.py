# Undoes the population script
# Will delete 
# - Activity and ActivityDependency
# - Module and ModuleDependency

import sqlite3
import sys

arguments = sys.argv
if len(arguments) < 2:
    print("Incorrect number of arguments: python3 [app.db]")
conn = sqlite3.connect(arguments[1])
cursor = conn.cursor()
if input("Do you want to delete the activities and their relationships? (y/n): ") == 'y':
    cursor.execute("DELETE FROM Activity")
    cursor.execute("DELETE FROM ActivityDependency")

if input("Do you want to delete the modules and their relationships? (y/n): ") == 'y':
    cursor.execute("DELETE FROM Module")
    cursor.execute("DELETE FROM ModuleDependency")

if input("Do you want to delete the users and their relationships? (y/n): ") == 'y':
    cursor.execute("DELETE FROM User")
    cursor.execute("DELETE FROM UserActivity")

conn.commit()
conn.close()