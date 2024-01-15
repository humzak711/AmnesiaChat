# AmnesiacChatroom
Amnesiac chatroom web application written in python using flask and flask_socketio

IMPORTANT

- This code assumes you are using a MySQL database, if not then change the code accordingly
- To setup your MySQL db credentials with the code, go to modules/config.py and input your MySQLdb credentials
- This code assumes you have a table in your MySQL database called 'users', which contains the columns; 'usernames', 'passwords' and 'recovery_keys'
- The chatrooms are designed to be amnesiac, any messages on the chat will dissapear once you reload the page
