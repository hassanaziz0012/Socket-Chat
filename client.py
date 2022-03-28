import socket
import threading


SERVER = socket.gethostbyname(socket.gethostname())
PORT = 5050
ADDR = (SERVER, PORT)

HEADER = 64
FORMAT = 'utf-8'
NAME = None


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

def receive_reply():
    while True:
        reply = client.recv(2048).decode(FORMAT)
        print(reply)

def send(message: str):
    msg = message.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(msg)


reply_thread = threading.Thread(target=receive_reply)
reply_thread.start()

if not NAME:
    msg = input("What's your name?")
    send(f"NAME:{msg}")

while True:
    msg = input("Message: ")
    send(msg)