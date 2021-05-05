# Undoes the population script
# Will delete 
# - Activity and ActivityDependency
# - Module and ModuleDependency

import sqlite3
import sys

arguments = sys.argv
if len(arguments) < 2:
    print("Incorrect number of arguments: python3 [app.db]")
sure = input("Are you sure you want to delete the entire database? (y/n)")
if sure != 'y':
    exit()
conn = sqlite3.connect(arguments[1])
cursor = conn.cursor()
cursor.execute("DELETE FROM Activity")
cursor.execute("DELETE FROM ActivityDependency")

cursor.execute("DELETE FROM Module")
cursor.execute("DELETE FROM ModuleDependency")

cursor.execute("DELETE FROM User")
cursor.execute("DELETE FROM UserActivity")

conn.commit()
conn.close()