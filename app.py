from flask import Flask, render_template, request, jsonify
import sys
sys.path.insert(0,"C:/laragon/bin/python/python-3.10/Scripts")
import pymysql


app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'wordpass'
app.config['MYSQL_DB'] = 'zeusdb'

mysql = pymysql.connect(
    host = app.config['MYSQL_HOST'],
    user = app.config['MYSQL_USER'],
    password= app.config['MYSQL_PASSWORD'],
    db = app.config['MYSQL_DB']
)

def create_table():
    cur = mysql.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS `zeusdb`.`college` (
      `CollegeCode` VARCHAR(8) NOT NULL,
      `CollegeName` VARCHAR(32) NOT NULL,
      PRIMARY KEY (`CollegeCode`),
      UNIQUE INDEX `CollegeName_UNIQUE` (`CollegeName` ASC) VISIBLE
    )""")

    cur.execute("""CREATE TABLE IF NOT EXISTS `zeusdb`.`course` (
      `CourseCode` VARCHAR(8) NOT NULL,
      `CourseName` VARCHAR(32) NOT NULL,
      `CollegeCode` VARCHAR(8) NOT NULL,
      PRIMARY KEY (`CourseCode`),
      UNIQUE INDEX `CourseName_UNIQUE` (`CourseName` ASC) VISIBLE,
      INDEX `CollegeCode_idx` (`CollegeCode` ASC) VISIBLE,
      CONSTRAINT `CollegeCode`
        FOREIGN KEY (`CollegeCode`)
        REFERENCES `zeusdb`.`college` (`CollegeCode`)
        ON DELETE NO ACTION
        ON UPDATE NO ACTION
    )""")

    cur.execute("""CREATE TABLE IF NOT EXISTS `zeusdb`.`student` (
      `StudentId` VARCHAR(8) NOT NULL,
      `StudentFirstName` VARCHAR(32) NOT NULL,
      `StudentLastName` VARCHAR(32) NOT NULL,
      `CourseCode` VARCHAR(8) NOT NULL,
      `StudentYearLvl` VARCHAR(4) NOT NULL,
      `StudentGender` VARCHAR(8) NOT NULL,
      PRIMARY KEY (`StudentId`),
      INDEX `CourseCode_idx` (`CourseCode` ASC) VISIBLE,
      CONSTRAINT `CourseCode`
        FOREIGN KEY (`CourseCode`)
        REFERENCES `zeusdb`.`course` (`CourseCode`)
        ON DELETE NO ACTION
        ON UPDATE NO ACTION
    )""")

    mysql.commit()
    cur.close()
        
@app.route("/")

def app_open():
    create_table()
    app.run(debug=True)
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
@app.route("/search", methods=['POST'])
def search():
    if request.method == 'POST':
        cur = mysql.cursor()
        search_query = request.form['search']

        # Add wildcards (%) to match partial strings
        search_query_with_wildcards = f"%{search_query}%"

        cur.execute("SELECT * FROM college WHERE collegecode LIKE %s OR collegename LIKE %s", (search_query_with_wildcards, search_query_with_wildcards))
        college_results = cur.fetchall()

        cur.execute("SELECT * FROM course WHERE coursecode LIKE %s OR coursename LIKE %s", (search_query_with_wildcards, search_query_with_wildcards))
        course_results = cur.fetchall()

        cur.execute("SELECT * FROM student WHERE studentid LIKE %s OR studentfirstname LIKE %s OR studentlastname LIKE %s OR studentyearlvl LIKE %s OR studentgender LIKE %s", (search_query_with_wildcards, search_query_with_wildcards, search_query_with_wildcards, search_query_with_wildcards, search_query_with_wildcards))
        student_results = cur.fetchall()

        results = {
            "college": college_results,
            "course": course_results,
            "student": student_results,
        }

        return render_template('searchresults.html', results=results)


# Functionalities -------------------------

# College --------------------------------
@app.route("/collegeaddtab", methods=['GET', 'POST'])
def collegeaddtab_open():
    return render_template('collegeaddtab.html')
@app.route('/collegesubmitadd', methods=['POST'])
def addcollege():
    if request.method == 'POST':
        cur = mysql.cursor()
        college_code = request.form['collegecode']
        college_name = request.form['collegename']

        if not college_code:
            return "College code cannot be empty"
        if not college_name:
            return "College name cannot be empty"

        cur.execute("SELECT * FROM college WHERE collegecode = %s", (college_code,))
        existing_college = cur.fetchone()
        if existing_college:
            return "College code already exists"

        cur.execute("SELECT * FROM course WHERE coursecode = %s", (college_code,))
        existing_course = cur.fetchone()
        if existing_course:
            return "College code is already used as a Course code"

        sql = "INSERT INTO college (collegecode, collegename) VALUES (%s, %s)"
        cur.execute(sql, (college_code, college_name))
        mysql.commit()
        cur.close()
        return "College added successfully"


@app.route("/collegedeletetab")
def collegedeletetab_open():
    return render_template('collegedeletetab.html')
@app.route('/collegesubmitdelete', methods=['POST'])
def delete_college():
    if request.method == 'POST':
        cur = mysql.cursor()
        college_code = request.form['collegecode']

        if not college_code:
            return "College code cannot be empty"

        cur.execute("SELECT * FROM college WHERE collegecode = %s", (college_code,))
        existing_college = cur.fetchone()
        if not existing_college:
            return "College code does not exist"

        cur.execute("SELECT * FROM course WHERE collegecode = %s", (college_code,))
        has_courses = cur.fetchone()
        if has_courses:
            return "Cannot delete this College because some courses belong in it."

        sql = "DELETE FROM college WHERE collegecode = %s"
        cur.execute(sql, (college_code,))
        mysql.commit()
        cur.close()
        return "College deleted successfully"


@app.route("/collegeedittab")
def collegeedittab_open():
    return render_template('collegeedittab.html')
@app.route('/collegesubmitedit', methods=['POST'])
def edit_college():
    if request.method == 'POST':
        cur = mysql.cursor()
        college_code = request.form['collegecode']
        new_college_name = request.form['collegename']

        if not college_code:
            return "College code is required."
        if not college_name:
            return "College name is required."

        cur.execute("SELECT * FROM college WHERE collegecode = %s", (college_code,))
        existing_college = cur.fetchone()
        if not existing_college:
            return "College code does not exist"

        cur.execute("SELECT * FROM course WHERE collegecode = %s", (college_code,))
        has_courses = cur.fetchone()
        if has_courses:
            return "Cannot edit this College because some courses belong in it."

        sql = "UPDATE college SET collegename = %s WHERE collegecode = %s"
        cur.execute(sql, (new_college_name, college_code))
        mysql.commit()
        cur.close()

        return "College name updated successfully"


@app.route("/collegelisttab")
def collegelisttab_open():
    cur = mysql.cursor()
    cur.execute("SELECT * FROM college")
    colleges = cur.fetchall()
    cur.close()
    return render_template('collegelisttab.html', colleges=colleges)


# Course --------------------------------
@app.route("/courseaddtab", methods=['GET', 'POST'])
def courseaddtab_open():
    return render_template('courseaddtab.html')
@app.route('/coursesubmitadd', methods=['POST'])
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


@app.route("/coursedeletetab")
def coursedeletetab_open():
    return render_template('coursedeletetab.html')
@app.route('/coursesubmitdelete', methods=['POST'])
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


@app.route("/courseedittab")
def courseedittab_open():
    return render_template('courseedittab.html')
@app.route('/coursesubmitedit', methods=['POST'])
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

@app.route("/courselisttab")
def courselisttab_open():
    cur = mysql.cursor()
    cur.execute("SELECT * FROM course")
    courses = cur.fetchall()
    cur.close()
    return render_template('courselisttab.html', courses=courses)


# Students --------------------------------
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