from flask import Flask, render_template, request, redirect
import json
import sqlite3

app = Flask(__name__)

with open("careers.json", "r") as file:
    careers = json.load(file)

@app.route("/", methods=["GET", "POST"])
def home():
    results = []
    name = ""

    if request.method == "POST":
        name = request.form["name"]
        skill = request.form["skill"].lower()
        interest = request.form["interest"].lower()
        cgpa = float(request.form["cgpa"])

        for career in careers:
            if skill in career["skills"] or interest == career["interest"]:
                results.append(career["career"])

        if cgpa >= 9:
            results.append("Eligible for top product companies")

        if len(results) == 0:
            results.append("No matching career found")

        final_result = ", ".join(results)

        conn = sqlite3.connect("responses.db")
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO students (name, skill, interest, cgpa, result) VALUES (?, ?, ?, ?, ?)",
            (name, skill, interest, cgpa, final_result)
        )

        conn.commit()
        conn.close()

    return render_template("index.html", results=results, name=name)

@app.route("/login", methods=["GET", "POST"])
def login():
    message = ""

    if request.method == "POST":
        if request.form["username"] == "admin" and request.form["password"] == "1234":
            return redirect("/dashboard")
        else:
            message = "Invalid Login"

    return render_template("login.html", message=message)

@app.route("/dashboard")
def dashboard():
    search = request.args.get("search", "")

    conn = sqlite3.connect("responses.db")
    cursor = conn.cursor()

    if search:
        cursor.execute("SELECT * FROM students WHERE name LIKE ?", ('%' + search + '%',))
    else:
        cursor.execute("SELECT * FROM students")

    data = cursor.fetchall()

    cursor.execute("SELECT COUNT(*) FROM students")
    total = cursor.fetchone()[0]

    conn.close()

    return render_template("dashboard.html", data=data, total=total)

@app.route("/delete/<int:id>")
def delete(id):
    conn = sqlite3.connect("responses.db")
    cursor = conn.cursor()

    cursor.execute("DELETE FROM students WHERE id=?", (id,))
    conn.commit()
    conn.close()

    return redirect("/dashboard")

if __name__ == "__main__":
    app.run(debug=True)