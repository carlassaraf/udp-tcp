import socket
import time
import sys
import threading

HEADER = 64
PORT = 8080
SERVER = '0.0.0.0'
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = '!DISCONNECT'


# TCP server
tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcp.bind(ADDR)

# UDP server
udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
udp.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
udp.bind(("", 8080))



def udp_server():
    while True:
        data, addr = udp.recvfrom(1024)
        
        data = data.decode('utf-8')
        print(f"[RECEIVED] : {data} from {addr}")
        
        if data == "getserverIP":
            udp.sendto(socket.gethostbyname(socket.gethostname()).encode('utf-8'), addr)

def confirm(conn):
    msg = "OK".encode(FORMAT)
    msg_length = len(msg)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    conn.send(send_length)
    conn.send(msg)

def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")

    connected = True
    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT)   # Blocking until we receive that number of bytes
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            if msg == DISCONNECT_MESSAGE:
                connected = False

            print(f"[{addr}] : {msg}")
            confirm(conn)
    
    conn.close()
    print(f"[DISCONNECT] {addr} disconnected.")
    sys.exit()


def tcp_server():
    tcp.listen(10)
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        conn, addr = tcp.accept()     
        confirm(conn)                                                       # Wait for a connection and save the connection and address
        thread = threading.Thread(target=handle_client, args=(conn, addr))  # Iniciate a new threat for every client
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")


udp_thread = threading.Thread(target=udp_server)
udp_thread.start()
print(f"[UDP SERVER STARTING]")

tcp_thread = threading.Thread(target=tcp_server)
tcp_thread.start()
print(f"[TCP SERVER STARTING]")





