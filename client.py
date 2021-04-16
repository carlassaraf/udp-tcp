import socket
import time

HEADER = 64
FORMAT = 'utf-8'

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)   # UDP
client.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

client.bind(("", 8080))
msg = "getserverIP".encode('utf-8')

NOT_ALLOWED = [
    ('192.168.0.224', 8080)
]

def send(msg, sock):
    # Send message
    message = msg.encode(FORMAT)                        # Encode the message in utf-8
    msg_length = len(message)                           # Get the length of the message
    send_length = str(msg_length).encode(FORMAT)        
    send_length += b' ' * (HEADER - len(send_length))   # Add the necessary bytes to get to the HEADER length
    sock.send(send_length)
    sock.send(message)
    
    # Receive confirmation
    msg_length = len(sock.recv(HEADER).decode(FORMAT))
    msg = sock.recv(msg_length).decode(FORMAT)
    print(f"[SERVER] : {msg}")

print("[BROADCASTING]")

while True:
    print('.')
    client.sendto(msg, ('<broadcast>', 8080))
    data, addr = client.recvfrom(1024)
    if addr not in NOT_ALLOWED: 
        print(f"[TCP SERVER IP] : {addr}")
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect(addr)
        connected = True
        while connected:
            msg = input()
            send(msg, client)
            if msg == 'close':
                connect = False
        break
    time.sleep(1)
    