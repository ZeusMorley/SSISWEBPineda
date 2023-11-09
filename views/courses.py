from flask import Blueprint, render_template, request, g, flash, redirect, url_for, jsonify

courses_bp = Blueprint('courses', __name__, template_folder='templates')

@courses_bp.route("/coursetab")
def coursetab_open():
    return render_template('course/coursetab.html')

@courses_bp.route("/courseaddtab", methods=['GET', 'POST'])
def courseaddtab_open():
    return render_template('course/courseaddtab.html')

@courses_bp.route("/coursedeletetab")
def coursedeletetab_open():
    return render_template('course/coursedeletetab.html')

@courses_bp.route("/courseedittab")
def courseedittab_open():
    return render_template('course/courseedittab.html')

@courses_bp.route('/coursesubmitadd', methods=['POST'])
def addcourse():
    flashed_messages = []
    mysql = g.get('mysql', None)
    if request.method == 'POST' and mysql:
        cur = mysql.cursor()
        course_code = request.form['coursecode'].upper()
        course_name = request.form['coursename']
        college_code = request.form['collegecode'].upper()
        
        if not course_code:
            flashed_messages.append(("Course code cannot be empty", 'error')) 
        if not college_code:
            flashed_messages.append(("College code cannot be empty", 'error')) 
        if not course_name:
            flashed_messages.append(("Course name cannot be empty", 'error')) 

        cur.execute("SELECT * FROM course WHERE coursecode = %s", (course_code,))
        existing_course = cur.fetchone()
        if existing_course:
            flashed_messages.append(("Course code already exists", 'error')) 

        cur.execute("SELECT * FROM college WHERE collegecode = %s", (course_code,))
        existing_college = cur.fetchone()
        if existing_college:
            flashed_messages.append(("Course code is already used as a College code", 'error')) 

        cur.execute("SELECT * FROM college WHERE collegecode = %s", (college_code,))
        existing_college = cur.fetchone()
        if not existing_college:
            flashed_messages.append(("College code does not exist.", 'error')) 

        if flashed_messages:
            return jsonify(flashes=flashed_messages)

        sql = "INSERT INTO course (coursecode, coursename, collegecode) VALUES (%s, %s, %s)"
        cur.execute(sql, (course_code, course_name, college_code))
        mysql.commit()
        cur.close()
        flashed_messages.append(("Course added successfully", 'success')) 

        if flashed_messages:
            return jsonify(flashes=flashed_messages)

    return jsonify(flashes=[])


@courses_bp.route('/coursesubmitdelete', methods=['POST'])
def delete_course():
    flashed_messages = []
    mysql = g.get('mysql', None)
    if request.method == 'POST' and mysql:
        cur = mysql.cursor()
        course_code = request.form['coursecode'].upper()
        
        if not course_code:
            flashed_messages.append(("Course code cannot be empty", 'error')) 

        cur.execute("SELECT * FROM course WHERE coursecode = %s", (course_code,))
        existing_course = cur.fetchone()
        if not existing_course:
            flashed_messages.append(("Course code does not exist", 'error')) 

        cur.execute("SELECT * FROM student WHERE coursecode = %s", (course_code,))
        has_students = cur.fetchone()
        if has_students:
            flashed_messages.append(("Cannot delete this Course because some students belong in it.", 'error')) 

        if flashed_messages:
            return jsonify(flashes=flashed_messages)

        sql = "DELETE FROM course WHERE coursecode = %s"
        cur.execute(sql, (course_code,))
        mysql.commit()
        cur.close()
        flashed_messages.append(("Course deleted successfully", 'success')) 

        if flashed_messages:
            return jsonify(flashes=flashed_messages)

    return jsonify(flashes=[])


@courses_bp.route('/coursesubmitedit', methods=['POST'])
def edit_course():
    flashed_messages = []
    existing_course_name = []
    existing_college_code = []
    mysql = g.get('mysql', None)
    if request.method == 'POST' and mysql:
        cur = mysql.cursor()
        course_code = request.form['coursecode'].upper()
        new_course_name = request.form['coursename']
        new_college_code = request.form['collegecode'].upper()
        
        if not course_code:
            flashed_messages.append(("Course code is required.", 'error'))
            return jsonify(flashes=flashed_messages)

        cur.execute("SELECT * FROM course WHERE coursecode = %s", (course_code,))
        existing_course = cur.fetchone()
        if not existing_course:
            flashed_messages.append(("Course code does not exist", 'error'))
            return jsonify(flashes=flashed_messages) 

        existing_course_name = existing_course[1]

        if new_course_name != '' and new_course_name != existing_course_name:
            sql = "UPDATE course SET coursename = %s WHERE coursecode = %s"
            cur.execute(sql, (new_course_name, course_code))
            mysql.commit()
            flashed_messages.append(("Course name updated successfully", 'success')) 
        elif new_course_name == '':
            flashed_messages.append(("No changes in Course name", 'success'))

        if new_college_code:
            cur.execute("SELECT * FROM college WHERE collegecode = %s", (new_college_code,))
            existing_college = cur.fetchone()
            if existing_college and existing_college[0] != existing_course[2]:
                existing_college_code = existing_college[0]
                sql = "UPDATE course SET collegecode = %s WHERE coursecode = %s"
                cur.execute(sql, (new_college_code, course_code))
                mysql.commit()
                flashed_messages.append(("College code updated successfully", 'success')) 
            elif not existing_college:
                flashed_messages.append(("College code does not exist", 'error'))
        else:
            flashed_messages.append(("No changes in College code", 'success'))

        return jsonify(flashes=flashed_messages)

    return jsonify(flashes=[])

@courses_bp.route('/courselisttab')
def courselisttab_open():
    mysql = g.get('mysql', None)
    if mysql:
        cur = mysql.cursor()
        cur.execute("SELECT * FROM course")
        courses = cur.fetchall()
        cur.close()
        return jsonify(courses=courses) 