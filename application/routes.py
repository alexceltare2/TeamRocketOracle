from application import app
from application.forms import BasicForm, StaffForm
from flask import render_template, request, g, flash, redirect, url_for
import pymysql
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash
import itertools
from datetime import datetime

# Section 2: HELPER FUNCTIONS e.g. DB connection code and methods
def connect_db():
    return pymysql.connect(
        user='root', password='password', database='team_rocket_project',
        autocommit=True, charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )

def get_db():
    '''Opens a new database connection per request.'''
    if not hasattr(g, 'db'):
        g.db = connect_db()
    return g.db

@app.teardown_appcontext
def close_db(error):
    '''Closes the database connection at the end of the request.'''
    if hasattr(g, 'db'):
        g.db.close()

# This retrieves users and passwords from the database to be paired and enumerated in the users and roles list
with app.app_context():
    my_cursor = get_db().cursor()
    my_cursor.execute("SELECT Staff_ID from staff")
    my_users = [index['Staff_ID'] for index in my_cursor.fetchall()]
    my_cursor.execute("SELECT Password from staff")
    my_passwords_hashed = [generate_password_hash(index['Password']) for index in my_cursor.fetchall()]
    my_cursor.execute("SELECT Staff_ID FROM staff WHERE Admin = 'Yes'")
    my_admins = [index['Staff_ID'] for index in my_cursor.fetchall()]

### HTTP Authorization
auth = HTTPBasicAuth()

users = dict(zip(my_users, my_passwords_hashed))
roles = dict(zip(my_users, itertools.repeat([])))
for i in roles.keys():
    if i in my_admins:
        roles[i] = ['admin']

@auth.verify_password
def verify_password(username, password):
    if username in users and check_password_hash(users.get(username), password):
        return username

@auth.get_user_roles
def get_user_roles(user):
    return roles[user]

# End HTTP Authorization

# Helper methods
# Section 4: APPLICATION ROUTES (WEB PAGE DEFINITIONS)

@app.route('/', methods=['GET', 'POST'])
@auth.login_required
def home():
    cursor = get_db().cursor()
    cursor.execute(f"SELECT job_ID, Customer_Last_Name, Address, Postcode FROM Jobs WHERE Staff_ID IN ('{auth.current_user()}') AND Is_Not_Done IS NULL")
    result = cursor.fetchall()
    if get_user_roles(auth.current_user())==['admin']:
        logged = "Admin"
    else:
        logged = "Engineer"
    return render_template(
        'home.html',
        title="Welcome to the Oracle job system.",
        description=f"You are logged in as {logged}.",
        records=result,
        user=auth.current_user(),
        role=get_user_roles(auth.current_user())
    )

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    return redirect(url_for('home')), 401


@app.route('/engineer_view', methods=['GET', 'POST'])
@auth.login_required
def engineer_view():
    cursor = get_db().cursor()
    cursor.execute("SELECT staff_ID, First_Name, Last_Name, Postcode, Phone_Number FROM Staff")
    result = cursor.fetchall()
    if get_user_roles(auth.current_user())==['admin']:
        logged = "Admin"
    else:
        logged = "Engineer"
    return render_template(
        'engineer_view.html',
        title="Welcome to the Engineer View.",
        description=f"You are logged in as {logged}.",
        records=result,
        user=auth.current_user(),
        role=get_user_roles(auth.current_user())
    )

@app.route('/staff/<id>')
@auth.login_required(role='admin')
def staff_display(id):
    cursor = get_db().cursor()
    cursor.execute("SELECT * FROM Staff WHERE staff_id=%s ", id)
    result = cursor.fetchone()
    cursor.execute("SELECT job_ID, Customer_Last_Name, Address, Postcode FROM Jobs WHERE Staff_ID=%s AND Is_Not_Done IS NULL", id)
    result2 = cursor.fetchall()
    return render_template(
                'staff.html',
                title="Staff info Card",
                description=f"Staff details provided below: {id}.",
                record=result,
                jobs=result2,
                role=get_user_roles(auth.current_user())
    )

def get_job_record_by_id(id):
    cursor = get_db().cursor()
    cursor.execute("SELECT job_ID, Customer_Last_Name, Address, Postcode, Phone_Number, Visit_Type, Staff_ID, Start_Time, End_Time FROM Jobs WHERE job_ID = %s", id)
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
            user=auth.current_user(),
            role=get_user_roles(auth.current_user())
        )
    else:
        return "Job not found"  # Or handle the case when the job record is not found

@app.route('/jobs/delete/<int:id>')
@auth.login_required(role='admin')
def jobs_delete(id):
    try:
        cursor = get_db().cursor()
        cursor.execute("DELETE FROM jobs WHERE job_ID=%s", id)
        message = f"Deleted jobs id {id}"
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
    if auth.current_user() == "admin":
        logged = "Admin"
    else:
        logged = "Engineer"
    return render_template(
        'engineer.html',
        title="Welcome to the Oracle job system.",
        description=f"You are logged in as {logged}.",
        records=result,
        user=auth.current_user(),
        role=get_user_roles(auth.current_user())
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
        try:
            cursor = get_db().cursor()
            sql = "INSERT INTO `jobs` (Customer_Last_Name, Address, Postcode, Phone_Number, Visit_Type, Staff_ID) VALUES (%s, %s, %s, %s, %s, %s)"
            cursor.execute(sql, (customer_last_name, address, postcode, phone_number, visit_type, staff_id))
            message = "Record successfully added"
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
        description='Please fill in all details, If no engineer is assigned to this job yet, this may be left blank. ',
        user=auth.current_user(),
        role=get_user_roles(auth.current_user())
    )

@app.route('/addstaff', methods=['GET', 'POST'])
@auth.login_required(role='admin')
def addstaff():
    message = ""
    form = StaffForm()
    if form.validate_on_submit():
        Staff_ID = form.Staff_ID.data
        First_Name = form.First_Name.data
        Last_Name = form.Last_Name.data
        Address = form.Address.data
        Postcode = form.Postcode.data
        Phone_Number = form.Phone_Number.data
        DTH_Skill = form.DTH_Skill.data
        BB_Skill = form.BB_Skill.data
        SE_Skill = form.SE_Skill.data
        MDU_Skill = form.MDU_Skill.data
        FTTP_Skilll = form.FTTP_Skilll.data
        Admin = form.Admin.data
        Password = form.Password.data
        try:
            cursor = get_db().cursor()
            sql = "INSERT INTO `staff` (Staff_ID, First_Name, Last_Name, Address, Postcode, Phone_Number, DTH_Skill, BB_Skill, SE_Skill, MDU_Skill, FTTP_Skilll, Admin, Password) VALUES (%s, %s, %s, %s, %s, %s, %s,%s,%s,%s,%s,%s,%s,)"
            cursor.execute(sql, (Staff_ID, First_Name, Last_Name, Address, Postcode, Phone_Number, DTH_Skill, BB_Skill, SE_Skill, MDU_Skill, FTTP_Skilll, Admin, Password))
            message = "Record successfully added"
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
        user=auth.current_user(),
        role=get_user_roles(auth.current_user())
    )

@app.route('/progress', methods=['GET', 'POST'])
@auth.login_required
def progress():
    cursor = get_db().cursor()
    cursor.execute(f"SELECT job_ID, Customer_Last_Name, Address, Postcode, Start_Time, End_Time, Is_Not_Done FROM Jobs WHERE Staff_ID=('{auth.current_user()}') AND Is_Not_Done IS NOT NULL")
    result = cursor.fetchall()
    if get_user_roles(auth.current_user())==['admin']:
        logged = "Admin"
    else:
        logged = "Engineer"
    return render_template(
        'progress.html',
        title="Welcome to the Oracle job system.",
        description=f"You are logged in as {logged}.",
        records=result,
        user=auth.current_user(),
        role=get_user_roles(auth.current_user())
    )

@app.route('/start_job/<int:id>', methods=['POST'])
@auth.login_required
def start_job(id):
    cursor = get_db().cursor()
    cursor.execute("SELECT Start_Time FROM Jobs WHERE job_ID = %s", id)
    start_time = cursor.fetchone()
    if start_time and start_time['Start_Time']:
        flash("Job already started at: " + str(start_time['Start_Time']))
    else:
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        try:
            cursor.execute("UPDATE Jobs SET Start_Time = %s WHERE job_ID = %s", (current_time, id))
            flash("Job started successfully!")
        except Exception as e:
            flash(f"Failed to start job: {e}")
    return redirect(url_for('home'))

@app.route('/end_job/<int:id>', methods=['POST'])
@auth.login_required
def end_job(id):
    cursor = get_db().cursor()
    cursor.execute("SELECT End_Time FROM Jobs WHERE job_ID = %s", id)
    end_time = cursor.fetchone()
    if end_time and end_time['End_Time']:
        flash("Job already Completed at: " + str(end_time['End_Time']))
    else:
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        try:
            cursor.execute("UPDATE Jobs SET End_Time = %s, Is_Not_Done = 'No' WHERE job_ID = %s", (current_time, id))
            flash("Job completed successfully!")
        except Exception as e:
            flash(f"Failed to end job: {e}")
    return redirect(url_for('home'))

@app.route('/is_not_done/<int:id>', methods=['POST'])
@auth.login_required
def is_not_done(id):
    cursor = get_db().cursor()
    cursor.execute("SELECT Is_Not_Done FROM Jobs WHERE job_ID = %s", id)
    is_not_done = cursor.fetchone()
    if is_not_done and is_not_done['Is_Not_Done']:
        flash("Job flagged as not done: " + str(is_not_done['Is_Not_Done']))
    else:
        try:
            cursor.execute("UPDATE Jobs SET Is_Not_Done = 'Yes' WHERE job_ID = %s", id)
            flash("Job Not Done!")
        except Exception as e:
            flash(f"Failed to flag job as not done: {e}")
    return redirect(url_for('home'))



