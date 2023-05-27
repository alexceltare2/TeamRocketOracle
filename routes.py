from application import app
from application.forms import BasicForm
from flask import render_template, request, g, flash, redirect, url_for
import pymysql
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash

### HTTP Authorization
auth = HTTPBasicAuth()

users = {
    "admin": generate_password_hash("admin"),
    "user": generate_password_hash("user")
}
roles = {
    "admin": ['admin'],
    "user": []
}

@auth.verify_password
def verify_password(username, password):
    if username in users and check_password_hash(users.get(username), password):
        return username

@auth.get_user_roles
def get_user_roles(user):
    return roles[user]
### End HTTP Authorization

# HELPER FUNCTIONS

def connect_db():
    return pymysql.connect(
        user='root', password='password', database='team_rocket_project',
        autocommit=True, charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )

def get_db():
    """Opens a new database connection per request."""
    if not hasattr(g, 'db'):
        g.db = connect_db()
    return g.db

@app.teardown_appcontext
def close_db(error):
    """Closes the database connection at the end of the request."""
    if hasattr(g, 'db'):
        g.db.close()

def get_date():
    """Function to return (fake) date - TASK: Update this - Add the code to pass the current date to the home HTML template."""
    today = "today"
    app.logger.info(f"In get_date function! Update so it returns the correct date! {today}")
    return today

# APPLICATION ROUTES

@app.route('/', methods=['GET', 'POST'])
@auth.login_required
def home():
    cursor = get_db().cursor()
    cursor.execute("SELECT job_ID, Customer_Last_Name, Address, Postcode FROM Jobs")
    result = cursor.fetchall()
    logged = "Admin" if auth.current_user() == "admin" else "Engineer"
    app.logger.info(result)
    return render_template(
        'home.html',
        title="Welcome to the Oracle job system.",
        description=f"You are logged in as {logged}.",
        records=result,
        user=auth.current_user()
    )


@app.route('/engineer_view', methods=['GET', 'POST'])
@auth.login_required
def engineer_view():
    cursor = get_db().cursor()
    cursor.execute("SELECT staff_ID, First_Name, Last_Name, Postcode, Phone_Number FROM Staff")
    result = cursor.fetchall()
    logged = "Admin" if auth.current_user() == "admin" else "Engineer"
    app.logger.info(result)
    return render_template(
        'engineer_view.html',
        title="Welcome to the Engineer View.",
        description=f"You are logged in as {logged}.",
        records=result,
        user=auth.current_user()
    )

@app.route('/progress', methods=['GET', 'POST'])
def progress():
    cursor = get_db().cursor()
    cursor.execute("SELECT staff_ID, First_Name, Last_Name, Postcode, Phone_Number FROM Staff")
    result = cursor.fetchall()
    app.logger.info(result)
    return render_template(
        'progress.html',
        title="Daily workload view.",
        description="Please ensure all jobs are allocated to capable engineers",
        records=result,
        user=auth.current_user()
    )

@app.route('/staff/<id>')
def staff_display(id):
    app.logger.info(id)
    cursor = get_db().cursor()
    cursor.execute("SELECT * FROM Staff WHERE staff_id=%s ", id)
    result = cursor.fetchone()
    app.logger.info(result)
    return render_template(
        'staff.html',
        title="Staff ID info Card.",
        description=f"Staff details provided below: staff_id={id}.",
        record=result
    )


def get_job_record_by_id(id):
    cursor = get_db().cursor()
    cursor.execute(
        "SELECT job_ID, Customer_Last_Name, Address, Postcode, Phone_Number, Visit_Type, Staff_ID, Start_Time, End_Time FROM Jobs WHERE job_ID = %s",
        (id,))
    record = cursor.fetchone()
    return record

@app.route('/jobs/display/<int:id>', methods=['GET'])
@auth.login_required
def jobs_display(id):
    job_record = get_job_record_by_id(id)
    if job_record:
        return render_template(
            'jobs.html',
            title="Job Details",
            record=job_record,
            user=auth.current_user()
        )
    else:
        return "Job not found"  # Or handle the case when the job record is not found

@app.route('/jobs/delete/<int:id>')
@auth.login_required(role='admin')
def jobs_delete(id):
    try:
        cursor = get_db().cursor()
        cursor.execute("DELETE FROM jobs WHERE job_ID=%s", (id,))
        message = f"Deleted jobs id {id}"
        app.logger.info(message)
        flash(message)
    except Exception as e:
        message = f"Error in delete operation: {e}"
        flash(message)
    return redirect(url_for('home'))

@app.route('/engineer', methods=['GET', 'POST'])
@auth.login_required
def engineer():
    cursor = get_db().cursor()
    cursor.execute("SELECT job_ID, Customer_Last_Name, Address, Postcode FROM Jobs")
    result = cursor.fetchall()
    logged = "Admin" if auth.current_user() == "admin" else "Engineer"
    app.logger.info(result)
    return render_template(
        'engineer.html',
        title="Welcome to the Oracle job system.",
        description=f"You are logged in as {logged}.",
        records=result,
        user=auth.current_user()
    )

@app.route('/addjob', methods=['GET', 'POST'])
@auth.login_required(role='admin')
def addjob():
    message = ""
    form = BasicForm()
    if form.validate_on_submit():
        customer_last_name = form.Customer_Last_Name.data
        address = form.Address.data
        postcode = form.Postcode.data
        phone_number = form.Phone_Number.data
        visit_type = form.Visit_Type.data
        staff_id = form.Staff_ID.data or "AAA00"
        app.logger.info(f"{customer_last_name} being added.")
        try:
            cursor = get_db().cursor()
            sql = "INSERT INTO `jobs` (Customer_Last_Name, Address, Postcode, Phone_Number, Visit_Type, Staff_ID) VALUES (%s, %s, %s, %s, %s, %s)"
            app.logger.info(sql)
            cursor.execute(sql, (customer_last_name, address, postcode, phone_number, visit_type, staff_id))
            message = "Record successfully added"
            app.logger.info(message)
            flash(message)
            return redirect(url_for('home'))
        except Exception as e:
            message = f"Error in insert operation: {e}"
            flash(message)
    return render_template(
        'form1.html',
        message=message,
        form=form,
        title='Job Creation Form.',
        description='Please fill in all details. If no engineer is assigned to this job yet, this may be left blank.',
        user=auth.current_user()
    )

@app.route('/addstaff', methods=['GET', 'POST'])
@auth.login_required(role='admin')
def addstaff():
    message = ""
    form = BasicForm()
    if form.validate_on_submit():
        Staff_ID = form.Staff_ID.data
        First_Name = form.First_Name.data
        Last_Name = form.Last_Name.data
        Address = form.Address.data
        Postcode = form.Postcode.data
        phone_number = form.Phone_Number.data
        DTH_Skill = form.DTH_Skill.data
        BB_Skill = form.BB_Skill.data
        SE_Skill = form.SE_Skill.data
        MDU_Skill = form.MDU_Skill.data
        FTTP_Skilll = form.FTTP_Skilll.data
        Admin = form.Admin.data
        Password = form.Password.data
        try:
            cursor = get_db().cursor()
            sql = "INSERT INTO `staff` (Staff_ID, First_Name, Last_Name, Address, Postcode, Phone_Number, DTH-Skill, BB_Skill, SE_Skill, MDU_Skill, FTTP_Skilll, Admin, Password) VALUES (%s, %s, %s, %s, %s, %s, %s,%s,%s,%s,%s,%s,%s,)"
            app.logger.info(sql)
            cursor.execute(sql, (Staff_ID, First_Name, Last_Name, Address, Postcode, Phone_Number, DTH_Skill, BB_Skill, SE_Skill, MDU_Skill, FTTP_Skilll, Admin, Password))
            message = "Record successfully added"
            app.logger.info(message)
            flash(message)
            return redirect(url_for('home'))
        except Exception as e:
            message = f"Error in insert operation: {e}"
            flash(message)
    return render_template(
        'form1.html',
        message=message,
        form=form,
        title='Staff Creation Form.',
        description='Please fill in all details. Do not leave any blank lines.',
        user=auth.current_user()
    )