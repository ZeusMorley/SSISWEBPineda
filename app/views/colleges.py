from flask import Blueprint, render_template, request

colleges_bp = Blueprint('colleges', __name__)

@colleges_bp.route("/collegetab")
def collegetab_open():
    return render_template('collegetab.html')


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
