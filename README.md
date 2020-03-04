# Multi-client Chatroom

A simple python3 based multi-client chatroom application built over the fundamentals of sockets in python.

*Developed as a part of the assessment for the module CST4045 Cross Platform Application Development at Middlesex University, London during the academic year 2019-20 under the guidance of module leader Dr Ralph Moseley.*

## Features
* Core
    * Multi-client
    * Admin authentication for server related activites
    * Full chatroom activity log
    * Individual user logs
    * User database w/ encrypted user passwords
    * Login system for returning users
* In-chat
    * Set or change preferred username
    * Set or change preferred password
    * Create, join or leave rooms
    * List users or rooms (admin only)
    * Send (encrypted) private messages

## Usage
1. Install dependencies
> pip3 install -r requirements.txt
2. Run server script
> python3 chat_server.py
3. Start server
    - Enter port number
    - Enter admin password
4. Run client script
> python3 chat_client.py [server_ip] [server_port]

## Client Options
```
/u [username]                       - Change the username
/p                                  - Change the password
/c [room_name]                      - Create a new room
/j [room_name]                      - Join a room
/l [room_name]                      - Leave a room
/cd [room_name]                     - Change default room
/list                               - (Admin) List all the rooms on the server
/users                              - (Admin) List all the users on the server
/public <[room_name]> [message]     - Sends a message to any room you are a part of
/private <[username]> [message]     - Send a (encrypted) private message to any user
/logout                             - Disconnect from the server
```

## Known Issues
There are certain known issues with respect to this code:
1. After running the server script, port number for the server has to be entered; some terminals print the line asking for the port number, others just keep waiting for the input without priting the line.
2. Getpass module issues a warning 'Warning: Password input may be echoed' on insecure terminals.
3. Incorrect login creates a new temporary user on the server.
4. The application is not yet fully compatible over the internet:
    - Same encryption key is used by the server and the client which is generated and stored on the server.
    - Some user validation takes place on the client side and needs to access the user database locally on the client side.
    
:heavy_exclamation_mark: **The code needs refactoring. Please note that this is my first python project and was written in a matter of just few hours.**
