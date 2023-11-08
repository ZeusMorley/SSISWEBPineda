from flask import Blueprint

colleges_bp = Blueprint('colleges', __name__, template_folder='templates/college')
courses_bp = Blueprint('courses', __name__, template_folder='templates/course')
students_bp = Blueprint('students', __name__, template_folder='templates/student')
search_bp = Blueprint('search', __name__, template_folder='templates/search')

from . import colleges, courses, students, search
