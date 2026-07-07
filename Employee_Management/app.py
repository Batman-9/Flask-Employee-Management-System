from flask import Flask, render_template, request, redirect
import mysql.connector

app = Flask(__name__)


connection = mysql.connector.connect(
    host="localhost",                 # WRITE YOUR HOST HERE
    user="root",
    password="YOUR_PASSWORD",               # WRITE YOUR PASSWORD HERE
    database="DATABASE_NAME"                # WRITE YOUR DATABASE NAME HERE
)

cursor = connection.cursor()


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/employees")
def employees():

    cursor.execute("SELECT * FROM employees")

    data = cursor.fetchall()

    return render_template(
        "employees.html",
        employees=data
    )

@app.route("/add", methods=["GET","POST"])
def add():

    if request.method == "POST":

        name = request.form["name"]
        email = request.form["email"]
        department = request.form["department"]
        salary = request.form["salary"]
        salary_date = request.form["salary_date"]

        sql = """
        INSERT INTO employees
        (Name,email,department,salary,Salary_credit_Date)
        VALUES(%s,%s,%s,%s,%s)
        """

        values = (
            name,
            email,
            department,
            salary,
            salary_date
        )

        cursor.execute(sql, values)
        connection.commit()

        return redirect("/employees")

    return render_template("add.html")

@app.route("/edit/<int:id>", methods=["GET","POST"])
def edit(id):

    if request.method == "POST":

        name = request.form["name"]
        email = request.form["email"]
        department = request.form["department"]
        salary = request.form["salary"]
        salary_date = request.form["salary_date"]

        sql = """
        UPDATE employees
        SET
        Name=%s,
        email=%s,
        department=%s,
        salary=%s,
        Salary_credit_Date=%s
        WHERE id=%s
        """

        values = (
            name,
            email,
            department,
            salary,
            salary_date,
            id
        )

        cursor.execute(sql, values)
        connection.commit()

        return redirect("/employees")

    cursor.execute(
        "SELECT * FROM employees WHERE id=%s",
        (id,)
    )

    employee = cursor.fetchone()

    return render_template(
        "edit.html",
        employee=employee
    )

@app.route("/delete/<int:id>")
def delete(id):

    cursor.execute(
        "DELETE FROM employees WHERE id=%s",
        (id,)
    )

    connection.commit()

    return redirect("/employees")

#---- Delete with Error Handling ----
@app.route("/employees/<int:id>", methods=["DELETE"])
def delete_employee(id):

    cursor.execute("SELECT * FROM employees WHERE id=%s",(id,))
    employee = cursor.fetchone()

    if employee is None:

        return jsonify({
            "error":"Employee Not Found"
        }),404

    cursor.execute(
        "DELETE FROM employees WHERE id=%s",
        (id,)
    )

    connection.commit()

    return jsonify({
        "message":"Employee Deleted Successfully"
    }),200

#---- Update with Error Handling ----
@app.route("/employees/<int:id>", methods=["PUT"])
def update_employee(id):

    cursor.execute(
        "SELECT * FROM employees WHERE id=%s",
        (id,)
    )

    employee = cursor.fetchone()

    if employee is None:

        return jsonify({
            "error":"Employee Not Found"
        }),404

    data = request.json

    sql = """
    UPDATE employees
    SET
    Name=%s,
    email=%s,
    department=%s,
    salary=%s,
    Salary_credit_Date=%s
    WHERE id=%s
    """

    values=(
        data["Name"],
        data["email"],
        data["department"],
        data["salary"],
        data["Salary_credit_Date"],
        id
    )

    cursor.execute(sql,values)
    connection.commit()

    return jsonify({
        "message":"Employee Updated Successfully"
    }),200

if __name__ == "__main__":
    app.run(debug=True)
