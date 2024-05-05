# code-along to a tutorial by Tech With Tim https://www.youtube.com/watch?v=3QiPPX-KeSc

import socket
import threading

# pick a port to run the server on
PORT = 5050

# ip address for devices to connect to - local network
SERVER = socket.gethostbyname(socket.gethostname())

# combine server and port into tuple
ADDR = (SERVER, PORT)

# open sockets for clients to connect
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# bind opened socket to address
server.bind(ADDR)

# header for receiving input from clients - contains the length of message that we receive from connections
HEADER = 64

# string that users send to indicate to server to disconnect them from the server
DISCONNECT = "/DISCONNECT"

active_connections = []
message_history = []

# handle connections
def handle_client(connection, addr):
    print(f"New connection connected from {addr}. ")
    connection.send("Connection successful".encode('utf-8'))
    connected = True

    # update new connections with chat history
    send_history(connection)

    # keep running while connection is up
    while connected:

        # first receives length of incoming message from client
        # .recv() does not run until recv has an input
        message_length = connection.recv(HEADER).decode('utf-8')

        # check if message_length is valid/has content
        if message_length:

            # convert message length into integer
            message_length = int(message_length)

            # receive the actual message
            message = connection.recv(message_length).decode('utf-8')

            print(f"{message}")

            # avoid propagating disconnect message
            if DISCONNECT in message:
                connected = False
                print(f"{addr} has disconnected from the server.")
            else:
                # store message in message history
                message_history.append(message)

                # if message is not disconnect message, send it out
                for c, a in active_connections:
                    if c == connection:
                        continue
                    else:
                        send_message(c, message)

        # handle disconnections properly - disconnect by sending a specific message 

    # close the connection
    connection.close()
    active_connections.remove((connection, addr))
    list_active_connections()

# listing out all current active connections
def list_active_connections():
    print("Active connections currently: ")
    for c, a in active_connections:
        print(a)

# for sending newly connected users the past chat history
def send_history(connection):
    for m in message_history:
        send_message(connection, m)

# to send message to connection
def send_message(connection, message):
    connection.send(message.encode('utf-8'))

# start up socket and handles connections
def start():
    server.listen()
    print(f"Server is listening on port {PORT} IP {SERVER}")

    # keep server listening
    while True:
        # server.accept() waits for a connection and returns the address of connectee
        connection, addr = server.accept()
        active_connections.append((connection, addr))
        # start a thread to handle client
        thread = threading.Thread(target=handle_client, args=(connection, addr), daemon=True)
        thread.start()
        print(f"Active connections: {threading.active_count() - 1}")

print("Starting server...")
start()