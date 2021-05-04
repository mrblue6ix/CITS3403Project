import sqlite3
import sys
import yaml

arguments = sys.argv
if len(arguments) < 3:
    print("Incorrect number of arguments: python3 [app.db] [modules.yaml]")
conn = sqlite3.connect(arguments[1])
cursor = conn.cursor()

# DIRECTORY STRUCTURE
# resources/
#   1-printing/
#       1-helloworld.yaml
#       2-variables.yaml
#       3-printingmultiple.yaml
#       4-userinput.yaml
#   2-numbers/
#       1-numbers.yaml

# CONTENTS OF modules.yaml file
# ---
# modules:
# - name: 1-printing
#   requires:
#   title: Printing in Python
#   description: For our first Python module, we will learn how to output to the terminal.
# - name: 2-numbers
#   requires:
#     - 1-printing
#   title: Numbers
#   description: In this module, we will learn how to work with numbers in Python
# - name: 3-strings
#   requires:
#     - 2-numbers
#   title: Strings
#   description: In this module, we will learn how to manipulate strings.
# - name: 4-lists
#   requires:
#     - 3-strings
#   title: Lists
#   description: We will learn how to use lists.
# ...
            
import yaml
# these are the folder to look in
with open(arguments[2]) as modules:
    try:
        modules = yaml.safe_load(modules)
    except yaml.YAMLError as exc:
        print(exc)
cursor.execute("SELECT * FROM Module")
print(cursor.fetchall())
for module in modules:
    m = modules[module]
    cursor.execute("SELECT * FROM Module WHERE name=?",(module,) )
    if cursor.fetchone() is None:
        cursor.execute("INSERT INTO Module(name, title, description) VALUES (?, ?, ?)",
                        (module, m['title'], m['description']))
                        
conn.commit()
conn.close()