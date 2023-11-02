from flask import Blueprint, render_template, request

students_bp = Blueprint('students', __name__)

@students_bp.route("/studenttab")
def studenttab_open():
    return render_template('studenttab.html')

@app.route("/studentaddtab")
def studentaddtab_open():
    return render_template('studentaddtab.html')
@app.route('/studentsubmitadd', methods=['POST'])
def addstudent():
    if request.method == 'POST':
        cur = mysql.cursor()
        student_id = request.form['studentid']
        student_first_name = request.form['studentfirstname']
        student_last_name = request.form['studentlastname']
        course_code = request.form['coursecode']
        student_year_level = request.form['studentyearlvl']
        student_gender = request.form['studentgender']

        if not student_id:
            return "Student ID cannot be empty"
        if not student_first_name:
            return "First name cannot be empty"
        if not student_last_name:
            return "Last name cannot be empty"
        if not course_code:
            return "Course code cannot be empty"

        cur.execute("SELECT * FROM course WHERE coursecode = %s", (course_code,))
        existing_course = cur.fetchone()
        if not existing_course:
            return "Course Code does not exist"

        if not student_year_level:
            return "Year level cannot be empty"
        if student_year_level not in ('1', '2', '3', '4'):
            return "Year level must be 1, 2, 3, or 4"
        if not student_gender:
            return "Gender cannot be empty"
        if not student_gender or student_gender.upper() not in ('MALE', 'FEMALE'):
            return "Gender must be either 'MALE' or 'FEMALE'."

        cur.execute("SELECT * FROM student WHERE studentid = %s", (student_id,))
        existing_student = cur.fetchone()
        if existing_student:
            return "Student ID already exists"

        sql = "INSERT INTO student (studentid, studentfirstname, studentlastname, coursecode, studentyearlvl, studentgender) VALUES (%s, %s, %s, %s, %s, %s)"
        cur.execute(sql, (student_id, student_first_name, student_last_name, course_code, student_year_level, student_gender))
        mysql.commit()
        cur.close()

        return "Student successfully added"

@app.route("/studentdeletetab")
def studentdeletetab_open():
    return render_template('studentdeletetab.html')
@app.route('/studentsubmitdelete', methods=['POST'])
def delete_student():
    if request.method == 'POST':
        cur = mysql.cursor()
        student_id = request.form['studentid']

        if not student_id:
            return "Student ID cannot be empty."

        cur.execute("SELECT * FROM student WHERE studentid = %s", (student_id,))
        existing_student = cur.fetchone()
        if not existing_student:
            return "Student ID does not exist"

        sql = "DELETE FROM student WHERE studentid = %s"
        cur.execute(sql, (student_id,))
        mysql.commit()
        cur.close()
        return "Student deleted successfully"

@app.route("/studentedittab")
def studentedittab_open():
    return render_template('studentedittab.html')
@app.route('/studentsubmitedit', methods=['POST'])
def edit_student():
    if request.method == 'POST':
        cur = mysql.cursor()
        student_id = request.form['studentid']
        new_student_first_name = request.form['studentfirstname']
        new_student_last_name = request.form['studentlastname']
        new_course_code = request.form['coursecode']
        new_student_year_level = request.form['studentyearlvl']
        new_student_gender = request.form['studentgender']

        if not student_id:
            return "Student ID cannot be empty"
        if not new_student_first_name:
            return "First name cannot be empty"
        if not new_student_last_name:
            return "Last name cannot be empty"
        if not new_course_code:
            return "Course code cannot be empty"

        cur.execute("SELECT * FROM course WHERE coursecode = %s", (new_course_code,))
        existing_course = cur.fetchone()
        if not existing_course:
            return "Course Code does not exist"

        if not new_student_year_level:
            return "Year level cannot be empty"
        if new_student_year_level not in ('1', '2', '3', '4'):
            return "Year level must be 1, 2, 3, or 4"
        if not new_student_gender:
            return "Gender cannot be empty"
        if not new_student_gender or new_student_gender.upper() not in ('MALE', 'FEMALE'):
            return "Gender must be either 'MALE' or 'FEMALE'."

        cur.execute("SELECT * FROM student WHERE studentid = %s", (student_id,))
        existing_student = cur.fetchone()
        if existing_student:
            return "Student ID already exists"

        sql = "UPDATE student SET studentfirstname = %s, studentlastname = %s, coursecode = %s, studentyearlvl = %s, studentgender = %s WHERE studentid = %s"
        cur.execute(sql, (new_student_first_name, new_student_last_name, new_course_code, new_student_year_level, new_student_gender))

        mysql.commit()
        cur.close()

        return "Student details updated successfully"

@app.route("/studentlisttab")
def studentlisttab_open():
    cur = mysql.cursor()
    cur.execute("SELECT * FROM student")
    students = cur.fetchall()
    cur.close()
    return render_template('studentlisttab.html', students=students)
