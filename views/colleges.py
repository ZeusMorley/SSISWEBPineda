from flask import Blueprint, render_template, request, g, flash, redirect, url_for, jsonify
import pymysql
colleges_bp = Blueprint('colleges', __name__, template_folder='templates')

@colleges_bp.route("/collegetab")
def collegetab_open():
    return render_template('college/collegetab.html')

@colleges_bp.route("/collegeaddtab", methods=['GET', 'POST'])
def collegeaddtab_open():
    return render_template('college/collegeaddtab.html')

@colleges_bp.route("/collegedeletetab")
def collegedeletetab_open():
    return render_template('college/collegedeletetab.html')

@colleges_bp.route("/collegeedittab")
def collegeedittab_open():
    return render_template('college/collegeedittab.html')


@colleges_bp.route('/collegesubmitadd', methods=['POST'])
def addcollege():
    flashed_messages = []
    mysql = g.get('mysql', None)
    if request.method == 'POST' and mysql:
        cur = mysql.cursor()
        college_code = request.form['collegecode'].upper()
        college_name = request.form['collegename']

        if not college_code:
            flashed_messages.append(("College code cannot be empty", 'error'))
        if not college_name:
            flashed_messages.append(("College name cannot be empty", 'error'))

        cur.execute("SELECT * FROM college WHERE collegecode = %s", (college_code,))
        existing_college = cur.fetchone()
        if existing_college:
            flashed_messages.append(("College code already exists", 'error'))

        cur.execute("SELECT * FROM course WHERE coursecode = %s", (college_code,))
        existing_course = cur.fetchone()
        if existing_course:
            flashed_messages.append(("College code is already used as a Course code", 'error'))

        if flashed_messages:
            return jsonify(flashes=flashed_messages)

        sql = "INSERT INTO college (collegecode, collegename) VALUES (%s, %s)"
        cur.execute(sql, (college_code, college_name))
        mysql.commit()
        cur.close()
        flashed_messages.append(("College added successfully", 'success'))

        if flashed_messages:
            return jsonify(flashes=flashed_messages)
        
    return jsonify(flashes=[])


@colleges_bp.route('/collegesubmitdelete', methods=['POST'])
def delete_college():
    flashed_messages = []
    mysql = g.get('mysql', None)
    if request.method == 'POST' and mysql:
        cur = mysql.cursor()
        college_code = request.form['collegecode'].upper()
        
        if not college_code:
            flashed_messages.append(("College code cannot be empty", 'error'))

        cur.execute("SELECT * FROM college WHERE collegecode = %s", (college_code,))
        existing_college = cur.fetchone()

        if not existing_college:
            flashed_messages.append(("College code does not exist", 'error'))

        cur.execute("SELECT * FROM course WHERE collegecode = %s", (college_code,))
        has_courses = cur.fetchone()
        if has_courses:
            flashed_messages.append(("Cannot delete this College because some courses belong in it.", 'error'))

        if flashed_messages:
            return jsonify(flashes=flashed_messages)

        sql = "DELETE FROM college WHERE collegecode = %s"
        cur.execute(sql, (college_code,))
        mysql.commit()
        cur.close()
        flashed_messages.append(("College deleted successfully", 'success'))

        if flashed_messages:
            return jsonify(flashes=flashed_messages)

    return jsonify(flashes=[])


@colleges_bp.route('/collegesubmitedit', methods=['POST'])
def edit_college():
    flashed_messages = []
    existing_college_name = []
    mysql = g.get('mysql', None)
    if request.method == 'POST' and mysql:
        cur = mysql.cursor()
        college_code = request.form['collegecode'].upper()
        new_college_name = request.form['collegename']
        
        if not college_code:
            flashed_messages.append(("College code is required.", 'error')) 

        cur.execute("SELECT * FROM college WHERE collegecode = %s", (college_code,))
        existing_college = cur.fetchone()
        if not existing_college:
            flashed_messages.append(("College code does not exist", 'error')) 
        else:
            existing_college_name = existing_college[1] 

        if flashed_messages:
            return jsonify(flashes=flashed_messages)

        if new_college_name != existing_college_name:
            sql = "UPDATE college SET collegename = %s WHERE collegecode = %s"
            cur.execute(sql, (new_college_name, college_code))
            mysql.commit()
            cur.close()
            flashed_messages.append(("College name updated successfully", 'success')) 
        else:
            flashed_messages.append(("No changes made to the College name", 'success'))

        if flashed_messages:
            return jsonify(flashes=flashed_messages)

    return jsonify(flashes=[])

@colleges_bp.route('/collegelisttab')
def collegelisttab_open():
    mysql = g.get('mysql', None)
    if mysql:
        cur = mysql.cursor()
        cur.execute("SELECT * FROM college")
        colleges = cur.fetchall()
        cur.close()
        return jsonify(colleges=colleges)