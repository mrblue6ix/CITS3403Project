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
cursor.execute("DELETE FROM Activity")
cursor.execute("DELETE FROM ActivityDependency")

cursor.execute("DELETE FROM Module")
cursor.execute("DELETE FROM ModuleDependency")

conn.commit()
conn.close()