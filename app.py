from flask import Flask
from flask import render_template

app = Flask(__name__)

@app.route("/")
def app_open():
    return render_template('index.html')

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
def searchtab():
    return render_template('searchtab.html')
