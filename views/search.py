from flask import Blueprint, render_template, request, g

search_bp = Blueprint('search', __name__)

@search_bp.route("/searchtab")
def searchtab_open():
    return render_template('searchtab.html')

@search_bp.route("/search", methods=['POST'])
def search():
    mysql = g.get('mysql', None)
    if request.method == 'POST' and mysql:
        cur = mysql.cursor()
        search_query = request.form['search']

        search_query_with_wildcards = f"%{search_query}%"

        cur.execute("""
            SELECT c.* 
            FROM college c
            WHERE c.collegecode LIKE %s OR c.collegename LIKE %s
        """, (search_query_with_wildcards, search_query_with_wildcards))
        college_results = cur.fetchall()

        cur.execute("""
            SELECT co.*, c.collegename 
            FROM course co
            LEFT JOIN college c ON co.collegecode = c.collegecode
            WHERE co.coursecode LIKE %s OR co.coursename LIKE %s
        """, (search_query_with_wildcards, search_query_with_wildcards))
        course_results = cur.fetchall()

        cur.execute("""
            SELECT s.*, co.coursename, c.collegename 
            FROM student s
            LEFT JOIN course co ON s.coursecode = co.coursecode
            LEFT JOIN college c ON co.collegecode = c.collegecode
            WHERE s.studentid LIKE %s 
            OR s.studentfirstname LIKE %s 
            OR s.studentlastname LIKE %s 
            OR s.studentyearlvl LIKE %s 
            OR s.studentgender LIKE %s
        """, (search_query_with_wildcards, search_query_with_wildcards, search_query_with_wildcards, search_query_with_wildcards, search_query_with_wildcards))
        student_results = cur.fetchall()

        results = {
            "college": college_results,
            "course": course_results,
            "student": student_results,
        }

        cur.execute("SELECT * FROM college WHERE collegecode LIKE %s OR collegename LIKE %s",
                    (search_query_with_wildcards, search_query_with_wildcards))
        college_results = cur.fetchall()

        if college_results:
            students_by_college = []
            courses_by_college = []

            for college in college_results:
                cur.execute("SELECT * FROM course WHERE collegecode = %s", (college[0],))
                courses_by_college.extend(cur.fetchall())

                cur.execute("SELECT * FROM student JOIN course ON student.coursecode = course.coursecode "
                            "WHERE course.collegecode = %s", (college[0],))
                students_by_college.extend(cur.fetchall())

            results = {
                "college": college_results,
                "course": courses_by_college,
                "student": students_by_college,
            }

        cur.execute("SELECT * FROM college WHERE collegecode LIKE %s OR collegename LIKE %s",
                    (search_query_with_wildcards, search_query_with_wildcards))
        college_results = cur.fetchall()

        if college_results:
            students_by_college = []
            courses_by_college = []

            for college in college_results:
                cur.execute("SELECT * FROM course WHERE collegecode = %s", (college[0],))
                courses_by_college.extend(cur.fetchall())

                cur.execute("""
                    SELECT s.*, co.coursename, c.collegename 
                    FROM student s
                    LEFT JOIN course co ON s.coursecode = co.coursecode
                    LEFT JOIN college c ON co.collegecode = c.collegecode
                    WHERE co.collegecode = %s
                """, (college[0],))
                students_by_college.extend(cur.fetchall())

            results = {
                "college": college_results,
                "course": courses_by_college,
                "student": students_by_college,
            }

            return render_template('searchresults.html', results=results)

        else:
            cur.execute("SELECT * FROM course WHERE coursecode LIKE %s OR coursename LIKE %s",
                        (search_query_with_wildcards, search_query_with_wildcards))
            course_results = cur.fetchall()

            cur.execute("SELECT * FROM student WHERE studentid LIKE %s OR studentfirstname LIKE %s "
                        "OR studentlastname LIKE %s OR studentyearlvl LIKE %s OR studentgender LIKE %s",
                        (search_query_with_wildcards, search_query_with_wildcards, search_query_with_wildcards,
                         search_query_with_wildcards, search_query_with_wildcards))
            student_results = cur.fetchall()

            results = {
                "college": college_results,
                "course": course_results,
                "student": student_results,
            }

        cur.execute("""
            SELECT c.* 
            FROM college c
            WHERE c.collegecode LIKE %s OR c.collegename LIKE %s
        """, (search_query_with_wildcards, search_query_with_wildcards))
        college_results = cur.fetchall()

        cur.execute("""
            SELECT co.*, c.collegename 
            FROM course co
            LEFT JOIN college c ON co.collegecode = c.collegecode
            WHERE co.coursecode LIKE %s OR co.coursename LIKE %s
        """, (search_query_with_wildcards, search_query_with_wildcards))
        course_results = cur.fetchall()

        cur.execute("""
            SELECT s.*, co.coursename, c.collegename 
            FROM student s
            LEFT JOIN course co ON s.coursecode = co.coursecode
            LEFT JOIN college c ON co.collegecode = c.collegecode
            WHERE s.studentid LIKE %s 
            OR s.studentfirstname LIKE %s 
            OR s.studentlastname LIKE %s 
            OR s.studentyearlvl LIKE %s 
            OR s.studentgender LIKE %s
            OR co.coursename LIKE %s 
            OR co.coursecode LIKE %s 
        """, (search_query_with_wildcards, search_query_with_wildcards, search_query_with_wildcards,
              search_query_with_wildcards, search_query_with_wildcards, search_query_with_wildcards,
              search_query_with_wildcards))
        student_results = cur.fetchall()

        results = {
            "college": college_results,
            "course": course_results,
            "student": student_results,
        }
        return render_template('searchresults.html', results=results)