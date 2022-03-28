import socket
import threading


SERVER = socket.gethostbyname(socket.gethostname())
PORT = 5050
ADDR = (SERVER, PORT)

HEADER = 64
FORMAT = 'utf-8'
DISCONNECT_MSG = "!DISCONNECT"

CLIENTS = []


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)


def handle_client(conn: socket.socket, addr: tuple):

    connected = True
    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            
            if msg.startswith("NAME:"):
                client_name = msg.replace("NAME:", "")
                CLIENTS.append({"conn": conn, "name": client_name})
            else:
                print(f"[NEW MESSAGE] {msg}")

                for client in CLIENTS:
                    print(f"Replying to {client['name']}")
                    sender = [client for client in CLIENTS if client['conn'] == conn][0]

                    client['conn'].send(f"{sender['name']}: {msg}\n".encode(FORMAT))

                if msg == DISCONNECT_MSG:
                    print(f"[CLOSING CONNECTION] {addr}")
                    connected = False
    conn.close()
    disconnect_requester = [client for client in CLIENTS if client['conn'] == conn][0]
    CLIENTS.remove(disconnect_requester)

def start():
    server.listen()
    print(f"[LISTENING] Listening on {SERVER}...")
    while True:
        conn, addr = server.accept()

        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()

        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")

        
start()