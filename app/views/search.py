from flask import Blueprint, render_template, request

search_bp = Blueprint('search', __name__)

@search_bp.route("/searchtab")
def searchtab_open():
    return render_template('searchtab.html')

@search_bp.route("/search", methods=['POST'])
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
