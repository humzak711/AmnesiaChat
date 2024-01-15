from flask import request, session, flash, render_template, Blueprint
from modules.SecurityChecks import hash_data, check_logged_in
from modules.config import db_connect

Login_blueprint = Blueprint('Login', __name__)

# Login page
@Login_blueprint.route('/login/', methods=['POST', 'GET']) 
def login():
    if request.method == 'POST':
        
        # retreive user inputs
        login_username = request.form['username']
        login_password = request.form['password']

        # format user inputs to match database
        login_username = login_username.strip()
        login_username = login_username.lower()
        hashed_password = hash_data(login_password)
        
        # Connect to database
        db = db_connect()
        cur = db.cursor()  # create cursor on mysqldb
        
        # check if login credentials already exist
        CredentialsExist = cur.execute("SELECT * FROM users WHERE usernames = %s AND passwords = %s", (login_username,hashed_password))
        cur.close() # close the cursor connection
        db.close() # close the database connection

        # if login credentials exist
        if CredentialsExist:
            if check_logged_in(): # log user out from previous session
                session.pop('logged_in', None)
                session.pop('username', None)
            session['logged_in'] = True
            session['username'] = login_username
            return render_template('login_successful.html')
        else:
            flash('ERROR: Login unsuccessful. Username or password incorrect')

    return render_template('login.html')