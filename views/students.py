from flask import Blueprint, render_template, request, g, flash, redirect, url_for, jsonify

students_bp = Blueprint('students', __name__, template_folder='templates')

@students_bp.route("/studenttab")
def studenttab_open():
    return render_template('student/studenttab.html')

@students_bp.route("/studentaddtab")
def studentaddtab_open():
    return render_template('student/studentaddtab.html')

@students_bp.route("/studentdeletetab")
def studentdeletetab_open():
    return render_template('student/studentdeletetab.html')

@students_bp.route("/studentedittab")
def studentedittab_open():
    return render_template('student/studentedittab.html')


@students_bp.route('/studentsubmitadd', methods=['POST'])
def addstudent():
    flashed_messages = []
    mysql = g.get('mysql', None)
    if request.method == 'POST' and mysql:
        cur = mysql.cursor()
        student_id = request.form['studentid']
        student_first_name = request.form['studentfirstname']
        student_last_name = request.form['studentlastname']
        course_code = request.form['coursecode']
        student_year_level = request.form['studentyearlvl']
        student_gender = request.form['studentgender']
        
        if not student_id:
            flashed_messages.append(("Student ID cannot be empty", 'error')) 
        if not student_first_name:
            flashed_messages.append(("First name cannot be empty", 'error')) 
        if not student_last_name:
            flashed_messages.append(("Last name cannot be empty", 'error')) 
        if not course_code:
            flashed_messages.append(("Course code cannot be empty", 'error')) 

        cur.execute("SELECT * FROM course WHERE coursecode = %s", (course_code,))
        existing_course = cur.fetchone()
        if not existing_course:
            flashed_messages.append(("Course Code does not exist", 'error')) 

        if not student_year_level:
            flashed_messages.append(("Year level cannot be empty", 'error')) 
        if student_year_level not in ('1', '2', '3', '4'):
            flashed_messages.append(("Year level must be 1, 2, 3, or 4", 'error')) 
        if not student_gender:
            flashed_messages.append(("Gender cannot be empty", 'error')) 
        if not student_gender or student_gender.upper() not in ('MALE', 'FEMALE'):
            flashed_messages.append(("Gender must be either 'MALE' or 'FEMALE'.", 'error')) 

        cur.execute("SELECT * FROM student WHERE studentid = %s", (student_id,))
        existing_student = cur.fetchone()
        if existing_student:
            flashed_messages.append(("Student ID already exists", 'error')) 

        if flashed_messages:
            return jsonify(flashes=flashed_messages)

        sql = "INSERT INTO student (studentid, studentfirstname, studentlastname, coursecode, studentyearlvl, studentgender) VALUES (%s, %s, %s, %s, %s, %s)"
        cur.execute(sql, (student_id, student_first_name, student_last_name, course_code, student_year_level, student_gender))
        mysql.commit()
        cur.close()
        flashed_messages.append(("Student successfully added", 'success')) 

        if flashed_messages:
            return jsonify(flashes=flashed_messages)
 
    return jsonify(flashes=[])


@students_bp.route('/studentsubmitdelete', methods=['POST'])
def delete_student():
    flashed_messages = []
    mysql = g.get('mysql', None)
    if request.method == 'POST' and mysql:
        cur = mysql.cursor()
        student_id = request.form['studentid']
        
        if not student_id:
            flashed_messages.append(("Student ID cannot be empty.", 'error')) 

        cur.execute("SELECT * FROM student WHERE studentid = %s", (student_id,))
        existing_student = cur.fetchone()
        if not existing_student:
            flashed_messages.append(("Student ID does not exist", 'error')) 

        if flashed_messages:
            return jsonify(flashes=flashed_messages)

        sql = "DELETE FROM student WHERE studentid = %s"
        cur.execute(sql, (student_id,))
        mysql.commit()
        cur.close()
        flashed_messages.append(("Student deleted successfully", 'success')) 

        if flashed_messages:
            return jsonify(flashes=flashed_messages)

    return jsonify(flashes=[])


@students_bp.route('/studentsubmitedit', methods=['POST'])
def edit_student():
    flashed_messages = []
    mysql = g.get('mysql', None)
    if request.method == 'POST' and mysql:
        cur = mysql.cursor()
        student_id = request.form['studentid']
        new_student_first_name = request.form['studentfirstname']
        new_student_last_name = request.form['studentlastname']
        new_course_code = request.form['coursecode']
        new_student_year_level = request.form['studentyearlvl']
        new_student_gender = request.form['studentgender']
        
        if not student_id:
            flashed_messages.append(("Student ID cannot be empty", 'error')) 
        if not new_student_first_name:
            flashed_messages.append(("First name cannot be empty", 'error')) 
        if not new_student_last_name:
            flashed_messages.append(("Last name cannot be empty", 'error')) 
        if not new_course_code:
            flashed_messages.append(("Course code cannot be empty", 'error')) 

        cur.execute("SELECT * FROM course WHERE coursecode = %s", (new_course_code,))
        existing_course = cur.fetchone()
        if not existing_course:
            flashed_messages.append(("Course Code does not exist", 'error')) 

        if not new_student_year_level:
            flashed_messages.append(("Year level cannot be empty", 'error')) 
        if new_student_year_level not in ('1', '2', '3', '4'):
            flashed_messages.append(("Year level must be 1, 2, 3, or 4", 'error')) 
        if not new_student_gender:
            flashed_messages.append(("Gender cannot be empty", 'error')) 
        if not new_student_gender or new_student_gender.upper() not in ('MALE', 'FEMALE'):
            flashed_messages.append(("Gender must be either 'MALE' or 'FEMALE'.", 'error')) 

        cur.execute("SELECT * FROM student WHERE studentid = %s", (student_id,))
        existing_student = cur.fetchone()
        if existing_student:
            flashed_messages.append(("Student ID already exists", 'error')) 

        if flashed_messages:
            return jsonify(flashes=flashed_messages)

        sql = "UPDATE student SET studentfirstname = %s, studentlastname = %s, coursecode = %s, studentyearlvl = %s, studentgender = %s WHERE studentid = %s"
        cur.execute(sql, (new_student_first_name, new_student_last_name, new_course_code, new_student_year_level, new_student_gender))
        mysql.commit()
        cur.close()
        flashed_messages.append(("Student details updated successfully", 'success')) 

        if flashed_messages:
            return jsonify(flashes=flashed_messages)

    return jsonify(flashes=[])


@students_bp.route('/studentlisttab')
def studentlisttab_open():
    mysql = g.get('mysql', None)
    if mysql:
        cur = mysql.cursor()
        cur.execute("SELECT * FROM student")
        students = cur.fetchall()
        cur.close()
        return render_template('student/studentlisttab.html', students=students)
    flashed_messages.append(("Student list endpoint", 'error')) 
