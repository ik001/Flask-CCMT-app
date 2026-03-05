from flask import Flask, render_template, request
import sqlite3
import math

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect("counselling.db")
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/", methods=["GET", "POST"])
def index():

    conn = get_db_connection()
    cursor = conn.cursor()

    # Dropdown values
    rounds = cursor.execute("SELECT DISTINCT round FROM counselling").fetchall()
    institutes = cursor.execute("SELECT DISTINCT institute FROM counselling").fetchall()
    programs = cursor.execute("SELECT DISTINCT program FROM counselling").fetchall()
    categories = cursor.execute("SELECT DISTINCT category FROM counselling").fetchall()

    # Default state
    round_filter = "All"
    institute_filter = "All"
    program_filter = "All"
    category_filter = "All"
    gate_score = ""
    search = ""
    entries = "10"
    page = 1

    rows = []
    total = 0
    total_pages = 0
    start_number = 0

    if request.method == "POST":

        round_filter = request.form.get("round", "All")
        institute_filter = request.form.get("institute", "All")
        program_filter = request.form.get("program", "All")
        category_filter = request.form.get("category", "All")
        gate_score = request.form.get("gate_score", "")
        search = request.form.get("search", "")
        entries = request.form.get("entries", "10")
        page = int(request.form.get("page", 1))

        base_query = " FROM counselling WHERE 1=1 "
        params = []

        if round_filter != "All":
            base_query += " AND round = ?"
            params.append(round_filter)

        if institute_filter != "All":
            base_query += " AND institute = ?"
            params.append(institute_filter)

        if program_filter != "All":
            base_query += " AND program = ?"
            params.append(program_filter)

        if category_filter != "All":
            base_query += " AND category = ?"
            params.append(category_filter)

        if gate_score:
            base_query += " AND min_gate_score <= ?"
            params.append(gate_score)

        if search:
            base_query += " AND (institute LIKE ? OR program LIKE ?)"
            params.extend([f"%{search}%", f"%{search}%"])

        # Count total rows
        count_query = "SELECT COUNT(*) " + base_query
        total = cursor.execute(count_query, params).fetchone()[0]

        # Pagination
        if entries != "All":
            limit = int(entries)
            offset = (page - 1) * limit
            data_query = "SELECT * " + base_query + " LIMIT ? OFFSET ?"
            rows = cursor.execute(data_query, params + [limit, offset]).fetchall()
            total_pages = math.ceil(total / limit) if limit else 1
            start_number = offset
        else:
            data_query = "SELECT * " + base_query
            rows = cursor.execute(data_query, params).fetchall()
            total_pages = 1
            start_number = 0

    conn.close()

    return render_template(
        "index.html",
        rows=rows,
        rounds=rounds,
        institutes=institutes,
        programs=programs,
        categories=categories,
        selected_round=round_filter,
        selected_institute=institute_filter,
        selected_program=program_filter,
        selected_category=category_filter,
        selected_gate_score=gate_score,
        search=search,
        entries=entries,
        page=page,
        total_pages=total_pages,
        total=total,
        start_number=start_number
        
@app.route("/sitemap.xml")
def sitemap():
    xml = render_template("sitemap.xml")
    return Response(xml, mimetype="application/xml")

if __name__ == "__main__":
    app.run()


