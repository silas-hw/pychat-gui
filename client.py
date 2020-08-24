import socket, pickle

USERNAME = 'test'

HEADER = 64
PORT = 5000
IP = '86.3.196.184'
ADDR = (IP, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!close"

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

def send(msg):
    message = pickle.dumps(msg)
    msgLength = len(message)
    sendLength = str(msgLength).encode(FORMAT)
    sendLength += b' ' * (HEADER-len(sendLength))
    client.send(sendLength)
    client.send(message)

def receive():
    msgHeader = client.recv(HEADER).decode(FORMAT)

    if msgHeader:
        msgLength = int(msgHeader)
        msg = client.recv(msgLength)

        if len(msg) == 0:
            return 0
            
        msg = pickle.loads(msg)
        return msg