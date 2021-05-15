import sqlite3
import sys
import yaml
import markdown
import os
import glob

# DIRECTORY STRUCTURE
# resources/
#   1-printing/
#       1-helloworld.yaml
#       2-variables.yaml
#       3-printingmultiple.yaml
#       4-userinput.yaml
#   2-numbers/
#       1-numbers.yaml
#   modules.yaml

arguments = sys.argv
if len(arguments) < 3:
    print("Incorrect number of arguments: python3 [app.db] [modules.yaml]")
conn = sqlite3.connect(arguments[1])
cursor = conn.cursor()

def toHtml(activity):
    if activity['prompt']:
        activity['prompt'] = markdown.markdown(activity['prompt'], extensions=['nl2br'])
    if activity['question']:
        activity['question'] = markdown.markdown(activity['question'], extensions=['nl2br'])
    return activity
            
# these are the folder to look in
with open(arguments[2]) as modules:
    try:
        modules = yaml.safe_load(modules)
    except yaml.YAMLError as exc:
        print(exc)

# Insert modules
print("Begin inserting Modules")
for module in modules:
    m = modules[module]
    cursor.execute("SELECT * FROM Module WHERE name=?",(module,) )
    if cursor.fetchone() is None:
        print(f"Inserting {module}")
        print(module)
        cursor.execute("INSERT INTO Module(name, title, description, is_test) VALUES (?, ?, ?, ?)",
                        (module, m['title'], m['description'], 'test-' in module))
print("Finished inserting Modules")

# Insert module dependancies
print("Inserting ModuleDependencies")
for module in modules:
    m = modules[module]
    requirements = m['requires']
    if requirements:
        child_id = cursor.execute('SELECT id FROM Module WHERE name=?', (module,))
        child_id = child_id.fetchone()[0]
        for r in requirements:
            parent_id = cursor.execute('SELECT id FROM Module WHERE name=?', (r,)) 
            parent_id = parent_id.fetchone()[0]
            cursor.execute('SELECT * FROM ModuleDependency WHERE parent=? AND child=?',
                             (parent_id, child_id))
            if cursor.fetchone() is None:
                print(f"Child ID: {child_id} Parent ID: {parent_id}")
                cursor.execute("INSERT INTO ModuleDependency(parent, child) VALUES (?, ?)",
                        (parent_id, child_id))
print("Finished inserting ModuleDependencies")

# Insert activities
print("Inserting Activities")
for module in modules:
    module_id = cursor.execute('SELECT id FROM Module WHERE name=?',(module,))
    module_id = cursor.fetchone()[0]
    # e.g resources/modules.yaml -> resources/1-1-printing
    folder = arguments[2].replace('modules.yaml', module) 
    if os.path.isdir(folder):
        for activity_file in glob.glob(f"{folder}/*.yaml"):
            activity_name = activity_file.split("/")[-1]
            cursor.execute("SELECT * FROM Activity WHERE name=?",
                            (activity_name.strip('.yaml'),))
            if cursor.fetchone() is None:
                with open(activity_file) as activity:
                    try:
                        a = yaml.safe_load(activity)
                        # Convert from Markdown to HTML
                        a = toHtml(a)
                        print(a)
                    except yaml.YAMLError as exc:
                        print(exc)
                print(f"Inserting {module}/{a['name']}")
                cursor.execute("INSERT INTO Activity(name,title, prompt, prefill, answer, solution, question, module_id) VALUES (?,?,?,?,?,?,?,?)",
                                (a['name'], a['title'], a['prompt'], a['prefill'],
                                 a['answer'], a['solution'], a['question'], module_id))
cursor.execute("UPDATE Activity SET times_submitted=0")
cursor.execute("UPDATE Activity SET times_right=0")
print("Finished inserting Activities")

# Insert activity dependencies
print("Inserting ActivityDependencies")
for module in modules:
    # e.g resources/modules.yaml -> resources/1-printing
    folder = arguments[2].replace('modules.yaml', module) 
    if os.path.isdir(folder):
        for activity_file in glob.glob(f"{folder}/*.yaml"):
            activity_name = os.path.basename(activity_file)
            with open(activity_file) as activity:
                try:
                    a = yaml.safe_load(activity)
                except yaml.YAMLError as exc:
                    print(exc)
            requirements = a['requires']
            if requirements:
                child_id = cursor.execute('SELECT id FROM Activity WHERE name=?', (activity_name.strip('.yaml'),))
                child_id = child_id.fetchone()[0]
                for r in requirements:
                    print(r)
                    parent_id = cursor.execute('SELECT id FROM Activity WHERE name=?', (r,))
                    parent_id = parent_id.fetchone()[0]
                    cursor.execute('SELECT * FROM ActivityDependency WHERE parent=? AND child=?',
                                    (parent_id, child_id))
                    if cursor.fetchone() is None:
                        print(f"Activity Child ID: {child_id} Parent ID: {parent_id}")
                        cursor.execute('INSERT INTO ActivityDependency(parent, child) VALUES (?, ?)',
                                        (parent_id, child_id))
print("Finished inserting ActivityDependies")

conn.commit()
conn.close()