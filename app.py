from flask import Flask, g, render_template
from db import create_table
from views.colleges import colleges_bp
from views.courses import courses_bp
from views.students import students_bp
from views.search import search_bp
import pymysql

app = Flask(__name__)
app.secret_key = 'secret'

# MySQL Configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'wordpass'
app.config['MYSQL_DB'] = 'zeusdb'

def create_mysql_connection():
    return pymysql.connect(
        host=app.config['MYSQL_HOST'],
        user=app.config['MYSQL_USER'],
        password=app.config['MYSQL_PASSWORD'],
        db=app.config['MYSQL_DB']
    )

@app.before_request
def before_request():
    g.mysql = create_mysql_connection()

@app.teardown_request
def teardown_request(exception):
    mysql = getattr(g, 'mysql', None)
    if mysql is not None:
        mysql.close()

# Register blueprints
app.register_blueprint(colleges_bp)
app.register_blueprint(courses_bp)
app.register_blueprint(students_bp)
app.register_blueprint(search_bp)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    create_table(create_mysql_connection())  # Creating tables at the start
    app.run(debug=True)
