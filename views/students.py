from flask import Blueprint, render_template, request, g, flash, redirect, url_for, jsonify
import re

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
        course_code = request.form['coursecode'].upper()
        student_year_level = request.form['studentyearlvl']
        student_gender = request.form['studentgender'].upper()
        
        student_id_pattern = re.compile(r'^20[0-2][0-9]-\d{4}$')

        if not student_id:
            flashed_messages.append(("Student ID cannot be empty", 'error')) 
        elif not student_id_pattern.match(student_id):
            flashed_messages.append(("Student ID should be in the format 'yyyy-xxxx' (e.g., 2021-1853)", 'error'))

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
    existing_first_name = []
    existing_last_name = []
    existing_course_code = []
    existing_yrlvl = []
    existing_gender = []
    mysql = g.get('mysql', None)
    if request.method == 'POST' and mysql:
        cur = mysql.cursor()
        student_id = request.form['studentid']
        new_student_first_name = request.form['studentfirstname']
        new_student_last_name = request.form['studentlastname']
        new_course_code = request.form['coursecode'].upper()
        new_student_year_level = request.form['studentyearlevel']
        new_student_gender = request.form['studentgender'].upper()

        student_id_pattern = re.compile(r'^20[0-2][0-9]-\d{4}$')

        if not student_id:
            flashed_messages.append(("Student ID cannot be empty", 'error')) 
        elif not student_id_pattern.match(student_id):
            flashed_messages.append(("Student ID should be in the format 'yyyy-xxxx' (e.g., 2021-1853)", 'error')) 
        
        cur.execute("SELECT * FROM student WHERE studentid = %s", (student_id,))
        existing_student = cur.fetchone()
        if not existing_student:
            flashed_messages.append(("Student ID does not exist", 'error'))
        else:
            existing_first_name = existing_student[1]
            existing_last_name = existing_student[2]
            existing_yrlvl = existing_student[4]
            existing_gender = existing_student[5]

        if new_student_first_name != '' and new_student_first_name != existing_first_name:
            sql = "UPDATE student SET studentfirstname = %s WHERE studentid = %s"
            cur.execute(sql, (new_student_first_name, student_id))
            mysql.commit()
            flashed_messages.append(("First name updated successfully", 'success')) 
        else:
            flashed_messages.append(("No changes in First name", 'success'))

        if new_student_last_name != '' and new_student_last_name != existing_last_name:
            sql = "UPDATE student SET studentlastname = %s WHERE studentid = %s"
            cur.execute(sql, (new_student_last_name, student_id))
            mysql.commit()
            flashed_messages.append(("Last name updated successfully", 'success')) 
        else:
            flashed_messages.append(("No changes in Last name", 'success'))

        if new_course_code:
            cur.execute("SELECT * FROM course WHERE coursecode = %s", (new_course_code,))
            existing_course = cur.fetchone()
            if existing_course and existing_course[0] != existing_student[3]:
                existing_course_code = existing_course[0]
                sql = "UPDATE student SET coursecode = %s WHERE studentid = %s"
                cur.execute(sql, (new_course_code, student_id))
                mysql.commit()
                flashed_messages.append(("Course code updated successfully", 'success')) 
            elif not existing_course:
                flashed_messages.append(("Course code does not exist", 'error'))
        else:
            flashed_messages.append(("No changes in Course code", 'success'))

        if new_course_code != '' and new_course_code != existing_course_code:
            cur.execute("SELECT * FROM course WHERE coursecode = %s", (new_course_code,))
            existing_course = cur.fetchone()
            if not existing_course:
                flashed_messages.append(("Course Code does not exist", 'error')) 
            else:
                sql = "UPDATE student SET coursecode = %s WHERE studentid = %s"
                cur.execute(sql, (new_course_code, student_id))
                mysql.commit()
                flashed_messages.append(("Course Code updated successfully", 'success')) 
        else:
            flashed_messages.append(("No changes in Course code", 'success'))

        if new_student_year_level != '' and new_student_year_level != existing_yrlvl:
            if new_student_year_level not in ('1', '2', '3', '4'):
                flashed_messages.append(("Year level must be 1, 2, 3, or 4", 'error'))
            else:
                sql = "UPDATE student SET studentyearlvl = %s WHERE studentid = %s"
                cur.execute(sql, (new_student_year_level, student_id))
                mysql.commit()
                flashed_messages.append(("Year level updated successfully", 'success'))
        else:
            flashed_messages.append(("No changes in Year level", 'success'))

        if new_student_gender != '' and new_student_gender != existing_gender:
            if new_student_gender.upper() not in ('MALE', 'FEMALE'):
                flashed_messages.append(("Gender must be either 'MALE' or 'FEMALE'.", 'error'))
            else:
                sql = "UPDATE student SET studentgender = %s WHERE studentid = %s"
                cur.execute(sql, (new_student_gender, student_id))
                mysql.commit()
                flashed_messages.append(("Gender updated successfully", 'success'))
        else:
            flashed_messages.append(("No changes in Gender", 'success')) 

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
        return jsonify(students=students) 