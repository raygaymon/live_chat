import socket
import threading
from colorama import Fore

# port that server is listening on
PORT = 5050

# ip address for devices to connect to - local network
SERVER = socket.gethostbyname(socket.gethostname())

# combine server and port into tuple
ADDR = (SERVER, PORT)

# header for receiving input from clients - contains the length of message that we receive from connections
HEADER = 64

# string that users send to indicate to server to disconnect them from the server
DISCONNECT = "/DISCONNECT"

# to connect to the server
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)
welcome_message = client.recv(2048).decode('utf-8')
if welcome_message:
    print(welcome_message)

username = input("Enter your desired username: ")
connected = True
print("Just enter your messages in the terminal. Enter '/DISCCONNECT to disconnect.")
sent_messages = set()
lock = threading.Lock()

# method to send message
def send_message(msg):

    msg = username + " : " + msg
    # encoding the string we send into utf-8 format
    message = msg.encode('utf-8')

    # sending the message length first
    message_length = len(message)

    # message that contains length of message
    send_length = str(message_length).encode('utf-8')

    # padding out send_length to 64 bytes by adding " " to fill up the difference in bytes
    send_length += b' ' * (HEADER - len(send_length))

    client.send(send_length)
    client.send(message)

    # add to list of messages
    sent_messages.add(msg)

def listen_for_message():

    while connected:

        incoming = client.recv(2048).decode('utf-8')

        if incoming:
            print(Fore.LIGHTRED_EX + f"\r\n{incoming}")

while connected:
        
    receive_thread = threading.Thread(target=listen_for_message, daemon=True)
    receive_thread.start()

    message = input()

    if len(message) < 1:
        continue

    if message == DISCONNECT:
        print("Disconnecting from the server.")
        send_message(message)
        connected = False
        continue

    send_message(message)





    

