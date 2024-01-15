from flask import request, session, flash, render_template, redirect, Blueprint
from modules.SecurityChecks import hash_data, generate_recovery_key
from modules.config import db_connect

AccountCreation_blueprint = Blueprint('AccountCreation', __name__)


# Sign-up page
@AccountCreation_blueprint.route('/signup/', methods=['POST', 'GET'])  
def signup():
    if request.method == 'POST':

        # clean session data 
        session.pop('signup_username', None)
        session.pop('signup_password', None)
        session.pop('signup_recovery_key', None)

        # retreive user inputs
        signup_username = request.form['username']
        signup_password = request.form['password']
        signup_re_password = request.form['re_password']
        
        # remove whitespace from inputs
        signup_username = signup_username.strip()
        signup_password = signup_password.strip()
        signup_re_password = signup_re_password.strip()
        # make username lowercase to match the database
        signup_username = signup_username.lower()
        
        # server side validation
        if signup_password != signup_re_password:
            flash('Re-entered password does not match the password.')
            return render_template('signup.html')
        
        # Connect to database
        db = db_connect()
        cur = db.cursor()  # create cursor on mysqldb

        # check if username already in use
        cur.execute("SELECT * FROM users WHERE usernames = %s", (signup_username))
        UsernameExist = cur.fetchone()
        cur.close() # close the cursor connection
        db.close() # close the database connection
        if UsernameExist:
            flash('ERROR: Sign up unsuccessful. Username already in use')
            return render_template('signup.html')
        else:
            signup_recovery_key = generate_recovery_key() # generate recovery key
            session['signup_username'] = signup_username
            session['signup_password'] = signup_password
            session['signup_recovery_key'] = signup_recovery_key
            return render_template('recovery_key.html', recovery_key=signup_recovery_key)
            
    return render_template('signup.html')

# Verify if recovery key is correct
@AccountCreation_blueprint.route('/verify_recovery_key/', methods=['POST'])
def verify_recovery_key():
    if request.method == 'POST':
        
        # retreive user inputs from recovery_key page
        entered_recovery_key = request.form['entered_recovery_key']
        
        # remove whitespace from entered recovery key
        entered_recovery_key = entered_recovery_key.strip()

        # retreive user inputs from signup page
        signup_recovery_key = session.get('signup_recovery_key')
        signup_password = session.get('signup_password')
        signup_username = session.get('signup_username')
        
        # if user input is correct, store credentials in database
        if signup_recovery_key == entered_recovery_key:

            # hash credentials
            hashed_password = hash_data(signup_password)
            hashed_recovery_key = hash_data(signup_recovery_key)
            
            # Connect to database
            db = db_connect()
            cur = db.cursor()  # create cursor on mysqldb
            
            # store data in database
            cur.execute("INSERT INTO users (usernames, passwords, recovery_keys) VALUES (%s,%s,%s)", (signup_username, hashed_password, hashed_recovery_key))
            db.commit() # commit the operation to store the new user credentials
            cur.close() # close the cursor connection
            db.close() # close the database connection
  
            # clean session data 
            session.pop('signup_username', None)
            session.pop('signup_password', None)
            session.pop('signup_recovery_key', None)

            # redirect user to login page
            return render_template('signup_successful.html')
        else:
            flash('ERROR: Please paste the recovery key correctly.')
            return render_template('recovery_key.html', recovery_key=signup_recovery_key) 
    else:
        return redirect('/404')
