from flask import Blueprint, render_template, session, redirect
from flask_socketio import join_room, leave_room, SocketIO,send
from modules.SecurityChecks import check_logged_in  
import secrets

Chatroom_blueprint = Blueprint('Chatroom', __name__)
socketio = SocketIO()

# Rooms dictionary to keep track of created rooms
rooms = {}

# Function to ensure room key is unique
def create_room_key() -> str:
    ''' Checks if room key already exists, if it does then the function recalls itself'''
    key = secrets.token_urlsafe(24)  # create long url safe room ID
    if key in rooms.keys():
        return create_room_key()
    else:
        return key
    

# Route to create a room
@Chatroom_blueprint.route('/room/create/')
def create_room():

    # ensure user is logged in
    username = session.get('username')
    if check_logged_in() and username:

        room_id = create_room_key() # set room_id as a unique url safe room key
        rooms[room_id] = set() # create room
        return redirect(f'/room/{room_id}')
    
    else:
        return render_template('login_redirect.html')

# Route to join a room
@Chatroom_blueprint.route('/room/<room_id>')
def join_room(room_id: str):

    # ensure user is logged in
    username = session.get('username')
    if check_logged_in() and username:
        if room_id in rooms.keys():

            session.pop('room_id', None) # clear session tokens
            session['room_id'] = room_id # set room_id session token
            return render_template('chatroom.html', username=username, room_id=room_id)
    
        else:
            return render_template('dashboard.html', username=username, ERROR='Error: Room does not exist')
    else:
        return render_template('login_redirect.html')
    

# Socket.IO event when a user connects
@socketio.on('connect')
def handle_connect():
    room_id = session.get('room_id')
    username = session.get('username')

    # add user to the room
    join_room(room_id)
    rooms[room_id].add(username)

    print(f'{username} connected to a room')
    send(f'{username} has joined the chat', room=room_id)

# Socket.IO event when a user disconnects
@socketio.on('disconnect')
def handle_disconnect():
    room_id = session.get('room_id')
    username = session.get('username')
    
    # check if user is connected to the room
    if room_id in rooms.keys():
        if username in rooms[room_id]:
            
            # remove user from the room
            leave_room(room_id)
            session.pop('room_id', None)
            rooms[room_id].remove(username)

            print(f'{username} disconnected from a room')
            send(f'{username} has left the chat', room=room_id)

# Socket.IO event for handling chat messages
@socketio.on('message')
def handle_chat_message(msg):
    room_id = session.get('room_id')
    username = session.get('username')

    print(f'Received message: {msg}')
    send({'msg': msg, 'name': username}, room=room_id)