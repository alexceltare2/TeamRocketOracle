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


# Helper methods
def get_date():
    """ Function to return (fake) date - TASK: Update this - Add the code to pass the current date to the home HTML template.
    """
    today = "Today"
    app.logger.info(f"In get_date function! Update so it returns the correct date! {today}")
    return today


# Section 4: APPLICATION ROUTES (WEB PAGE DEFINITIONS)

@app.route('/', methods=['GET', 'POST'])
@auth.login_required
def home():
    cursor = get_db().cursor()
    cursor.execute("SELECT job_ID, Customer_Last_Name, Address, Postcode FROM Jobs")
    result = cursor.fetchall()
    if auth.current_user() == "admin":
        logged = "Admin"
    else:
        logged = "Engineer"
    app.logger.info(result)
    return render_template(
        'home.html',
        title="Welcome to the Oracle job system.",
        description=f"You are logged in as {logged}.",
        records=result,
        user=auth.current_user()
    )

@app.route('/register1', methods=['GET', 'POST'])
@auth.login_required
def register():
    """ Basic form.
    """
    error = ""
    form = BasicForm()  # create form instance

    if request.method == "POST":
        first_name = form.first_name.data
        last_name = form.last_name.data

        app.logger.info(f"We were given: {first_name} {last_name}")

        if len(first_name) == 0 or len(last_name) == 0:
            error = "Please supply both first and last names."
        else:
            return 'Thank you!'

    return render_template(
        'form1.html',
        title="Simple form!",
        description=f"Using Flask with a form on {get_date()}",
        form=form,
        message=error,
        user=auth.current_user()
    )

@app.route('/register2', methods=['GET', 'POST'])
@auth.login_required(role='admin')
def register2():
    """ Second form.
    """
    message = ""
    form = BasicForm()  # create form instance
    if form.validate_on_submit():
        first_name = form.first_name.data
        last_name = form.last_name.data
        app.logger.info(f"{first_name} {last_name} being added.")
        try:
            cursor = get_db().cursor()
            sql = "INSERT INTO `jobs` (first_name, last_name) VALUES (%s, %s)"
            app.logger.info(sql)
            cursor.execute(sql, (first_name.upper(), last_name.upper()))
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
        title='Form Test 2 - Add',
        description='DB test',
        user=auth.current_user()
    )

def get_job_record_by_id(id):
    cursor = get_db().cursor()
    cursor.execute("SELECT job_ID, Customer_Last_Name FROM Jobs WHERE job_ID = %s", (id,))
    record = cursor.fetchone()
    return record

@app.route('/jobs/display/<int:id>', methods=['GET'])
@auth.login_required
def jobs_display(id):
    # Logic to retrieve job record by ID and assign it to the `job_record` variable
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
    """ Fourth route. Param for deleting from jobs table
    """
    app.logger.info(id)
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
    if auth.current_user() == "admin":
        logged = "Admin"
    else:
        logged = "Engineer"
    app.logger.info(result)
    return render_template(
        'engineer.html',
        title="Welcome to the Oracle job system.",
        description=f"You are logged in as {logged}.",
        records=result,
        user=auth.current_user()
    )
