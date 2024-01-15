from flask import Flask
from flask_socketio import SocketIO
from blueprints.Home import Home_blueprint
from blueprints.AccountCreation import AccountCreation_blueprint
from blueprints.Login import Login_blueprint
from blueprints.AccountRecovery import AccountRecovery_blueprint
from blueprints.Dashboard import Dashboard_blueprint
from blueprints.Chatroom import Chatroom_blueprint

# Create the Flask application
app = Flask(__name__)  
socketio = SocketIO(app,cors_allowed_origins="*")  # Allow connections from all origins (*)
app.secret_key = 'hpwoeksjkbjdvx372trwysv23s33378jvbuguyefyeyefagvshvehvha7637637rvwghwcg22'
 
# Register blueprints
app.register_blueprint(Home_blueprint) # Front page
app.register_blueprint(AccountCreation_blueprint) # Signup 
app.register_blueprint(Login_blueprint) # Login
app.register_blueprint(AccountRecovery_blueprint) # Password reset
app.register_blueprint(Dashboard_blueprint) # User dashboard

# API to handle creating, joining chatrooms and chatroom functionality
app.register_blueprint(Chatroom_blueprint) 

# Run the web application 
if __name__ == '__main__':  
    socketio.run(app,debug=True)


# to do:
# make it so the messages actually render on the chatroom
 
# implement rate limitation