from flask import Blueprint, render_template, session, redirect
from modules.SecurityChecks import check_logged_in  

Dashboard_blueprint = Blueprint('Dashboard', __name__)


# Dashboard accessible if logged in
@Dashboard_blueprint.route('/dashboard/', methods=['POST','GET'])
def dashboard():
    if check_logged_in():
        username = session.get('username')
        return render_template('dashboard.html', username=username)
    else: # redirect to login page if user is not logged in
        return render_template('login_redirect.html')
    
# Logout
@Dashboard_blueprint.route('/logout/')
def logout():
    if check_logged_in():
        # clean session tokens
        session.pop('logged_in', None)
        session.pop('username', None) 
        return render_template('index.html')
    else:
        return redirect('/404')