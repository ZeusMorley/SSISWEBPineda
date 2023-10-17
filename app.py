from flask import Flask
from flask import render_template

app = Flask(__name__)

@app.route("/")
def app_open():
    return render_template('index.html')

# Homes Tabs ------------------------------

@app.route("/studenttab")
def studenttab_open():
    return render_template('studenttab.html')

@app.route("/coursetab")
def coursetab_open():
    return render_template('coursetab.html')

@app.route("/collegetab")
def collegetab_open():
    return render_template('collegetab.html')

@app.route("/searchtab")
def searchtab_open():
    return render_template('searchtab.html')


# Functionalities -------------------------

# College --------------------------------
@app.route("/collegeaddtab")
def collegeaddtab_open():
    return render_template('collegeaddtab.html')

@app.route("/collegedeletetab")
def collegedeletetab_open():
    return render_template('collegedeletetab.html')

@app.route("/collegeedittab")
def collegeedittab_open():
    return render_template('collegeedittab.html')

@app.route("/collegelisttab")
def collegelisttab_open():
    return render_template('collegelisttab.html')


# Course --------------------------------
@app.route("/courseaddtab")
def courseaddtab_open():
    return render_template('courseaddtab.html')

@app.route("/coursedeletetab")
def coursedeletetab_open():
    return render_template('coursedeletetab.html')

@app.route("/courseedittab")
def courseedittab_open():
    return render_template('courseedittab.html')

@app.route("/courselisttab")
def courselisttab_open():
    return render_template('courselisttab.html')


# Students --------------------------------
@app.route("/studentaddtab")
def studentaddtab_open():
    return render_template('studentaddtab.html')

@app.route("/studentdeletetab")
def studentdeletetab_open():
    return render_template('studentdeletetab.html')

@app.route("/studentedittab")
def studentedittab_open():
    return render_template('studentedittab.html')

@app.route("/studentlisttab")
def studentlisttab_open():
    return render_template('studentlisttab.html')
