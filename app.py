from flask import Flask
from db import create_table

app = Flask(__name__)

# Import blueprints
from views.colleges import colleges_bp
from views.courses import courses_bp
from views.students import students_bp
from views.search import search_bp

# Register blueprints
app.register_blueprint(colleges_bp)
app.register_blueprint(courses_bp)
app.register_blueprint(students_bp)
app.register_blueprint(search_bp)

if __name__ == '__main__':
    create_table()
    app.run(debug=True)
