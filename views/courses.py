from flask import Blueprint, render_template, request

courses_bp = Blueprint('courses', __name__, template_folder='templates')

@courses_bp.route("/coursetab")
def coursetab_open():
    return render_template('course/coursetab.html')


@courses_bp.route("/courseaddtab", methods=['GET', 'POST'])
def courseaddtab_open():
    return render_template('course/courseaddtab.html')


@courses_bp.route('/coursesubmitadd', methods=['POST'])
def addcourse():
    if request.method == 'POST':
        cur = mysql.cursor()
        course_code = request.form['coursecode']
        course_name = request.form['coursename']
        college_code = request.form['collegecode']

        if not course_code:
            return "Course code cannot be empty"
        if not college_code:
            return "College code cannot be empty"
        if not course_name:
            return "Course name cannot be empty"

        cur.execute("SELECT * FROM course WHERE coursecode = %s", (course_code,))
        existing_course = cur.fetchone()
        if existing_course:
            return "Course code already exists"

        cur.execute("SELECT * FROM college WHERE collegecode = %s", (course_code,))
        existing_college = cur.fetchone()
        if existing_college:
            return "Course code is already used as a College code"

        cur.execute("SELECT * FROM college WHERE collegecode = %s", (college_code,))
        existing_college = cur.fetchone()
        if not existing_college:
            return "College code does not exist."

        sql = "INSERT INTO course (coursecode, coursename, collegecode) VALUES (%s, %s, %s)"
        cur.execute(sql, (course_code, course_name, college_code))
        mysql.commit()
        cur.close()
        return "Course added successfully"


@courses_bp.route("/coursedeletetab")
def coursedeletetab_open():
    return render_template('course/coursedeletetab.html')


@courses_bp.route('/coursesubmitdelete', methods=['POST'])
def delete_course():
    if request.method == 'POST':
        cur = mysql.cursor()
        course_code = request.form['coursecode']

        if not course_code:
            return "Course code cannot be empty"

        cur.execute("SELECT * FROM course WHERE coursecode = %s", (course_code,))
        existing_course = cur.fetchone()
        if not existing_course:
            return "Course code does not exist"

        cur.execute("SELECT * FROM student WHERE coursecode = %s", (course_code,))
        has_students = cur.fetchone()
        if has_students:
            return "Cannot delete this Course because some students belong in it."

        sql = "DELETE FROM course WHERE coursecode = %s"
        cur.execute(sql, (course_code,))
        mysql.commit()
        cur.close()
        return "Course deleted successfully"


@courses_bp.route("/courseedittab")
def courseedittab_open():
    return render_template('course/courseedittab.html')


@courses_bp.route('/coursesubmitedit', methods=['POST'])
def edit_course():
    if request.method == 'POST':
        cur = mysql.cursor()
        course_code = request.form['coursecode']
        new_course_name = request.form['coursename']
        new_college_code = request.form['collegecode']

        if not course_code:
            return "Course code is required."
        if not new_course_name:
            return "Course name is required."
        if not new_college_code:
            return "College code is required."

        cur.execute("SELECT * FROM course WHERE coursecode = %s", (course_code,))
        existing_course = cur.fetchone()
        if not existing_course:
            return "Course code does not exist"

        cur.execute("SELECT * FROM student WHERE coursecode = %s", (course_code,))
        has_students = cur.fetchone()
        if has_students:
            return "Cannot edit this Course because some students belong in it."

        cur.execute("SELECT * FROM college WHERE collegecode = %s", (new_college_code,))
        existing_college = cur.fetchone()
        if not existing_college:
            return "College code does not exist"

        sql = "UPDATE course SET coursename = %s, collegecode = %s WHERE coursecode = %s"
        cur.execute(sql, (new_course_name, new_college_code, course_code))

        mysql.commit()
        cur.close()

        return "Course details updated successfully"


@courses_bp.route("/courselisttab")
def courselisttab_open():
    cur = mysql.cursor()
    cur.execute("SELECT * FROM course")
    courses = cur.fetchall()
    cur.close()
    return render_template('course/courselisttab.html', courses=courses)


from courses import courses_bp
app.register_blueprint(courses_bp)