import select
import socket
import sys
from getpass import getpass
from cryptography.fernet import Fernet
from tinydb import TinyDB, Query

file = open('log/key.key', 'rb')
key = file.read()
file.close()
cipher_suite = Fernet(key)

db = TinyDB('log/users.json')

BUFFER_SIZE = 4096


def chat(h, p):
    host = str(h)
    port = int(p)
    client_connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_connection.settimeout(5)
    try:
        client_connection.connect((host, port))
    except socket.error:
        print("Unable to connect!")
        sys.exit(0)
    print("Connected to the server!")
    is_user = False
    while True:
        username = input("Username: ")
        user_query = Query()
        result = db.search(user_query.username == username)
        for r in result:
            if r['username']:
                password = getpass()
                if r['password'] == "" and password == "":
                    client_connection.send((r['username'] + " EXISTS").encode())
                    print(client_connection.recv(BUFFER_SIZE).decode())
                    is_user = True
                    break
                else:
                    if cipher_suite.decrypt(r['password'].encode()) == password.encode():
                        client_connection.send((r['username'] + " EXISTS").encode())
                        print(client_connection.recv(BUFFER_SIZE).decode())
                        is_user = True
                        break
                    else:
                        print("Wrong password!")
                        sys.exit(0)
            else:
                sys.exit(0)
        if is_user:
            break
        elif len(username.strip()) != 0:
            client_connection.send(username.encode())
            print(client_connection.recv(BUFFER_SIZE).decode())
            break
        else:
            continue
    print("Type /help to display the list of available commands.")
    sys.stdout.write("> ")
    sys.stdout.flush()
    while True:
        sockets_list = [sys.stdin, client_connection]
        r, w, e = select.select(sockets_list, [], [])
        for notified_socket in r:
            if notified_socket == client_connection:
                data = client_connection.recv(BUFFER_SIZE).decode()
                if data == "GETADMINPASS":
                    tmp_pass = getpass("Admin Password: ")
                    client_connection.send(tmp_pass.encode())
                    sys.stdout.write("> ")
                    sys.stdout.flush()
                elif data == "GETUSERPASS":
                    tmp_pass = getpass("New Password: ")
                    client_connection.send(tmp_pass.encode())
                    sys.stdout.write("> ")
                    sys.stdout.flush()
                elif data.partition("gAAAA")[2]:
                    decrypted_messaged = cipher_suite.decrypt(data.encode())
                    sys.stdout.write(decrypted_messaged.decode())
                    sys.stdout.write("\n")
                    sys.stdout.write("> ")
                    sys.stdout.flush()
                elif data:
                    sys.stdout.write(data)
                    sys.stdout.write("> ")
                    sys.stdout.flush()
                else:
                    print("You have been disconnected from the  server!")
                    sys.exit(0)
            else:
                message = sys.stdin.readline()
                if message == '/logout\n':
                    client_connection.send("/quit".encode())
                    print("[SERVER] You have been disconnected from the server!")
                    sys.exit(0)
                elif message == '/help\n':
                    list_commands()
                    sys.stdout.write("> ")
                    sys.stdout.flush()
                else:
                    client_connection.send(message.encode())
                    sys.stdout.write("> ")
                    sys.stdout.flush()


def list_commands():
    print("/u [username]                      - Change the username"
          "\n/p                                 - Change the password"
          "\n/c [room_name]                     - Create a new room"
          "\n/j [room_name]                     - Join a room"
          "\n/l [room_name]                     - Leave a room"
          "\n/cd [room_name]                    - Change default room"
          "\n/list                              - (Admin) List all the rooms on the server"
          "\n/users                             - (Admin) List all the users on the server"
          "\n/public <[room_name]> [message]    - Sends a message to any room you are a part of"
          "\n/private <[username]> [message]    - Send a private (encrypted) message to any user"
          "\n/logout                            - Disconnect from the server")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Please enter the server host and port number as arguments!"
              "\nUsage: python3 chat_client.py [host] [port]"
              "\nExample: python3 chat_client.py 127.0.0.1 9999")
        sys.exit(0)
    try:
        chat(sys.argv[1], sys.argv[2])
    except KeyboardInterrupt:
        print("\nClient Disconnected!")
