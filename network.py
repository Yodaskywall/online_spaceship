import socket
import pickle

HEADERSIZE = 10

def pickle_send(conn, object):
    msg = pickle.dumps(object)
    msg = bytes(f"{len(msg):<{HEADERSIZE}}", "utf-8") + msg
    conn.send(msg)


def pickle_receive(conn):
    full_msg = b''
    new_msg = True
    while True:
        msg = conn.recv(16)

        if new_msg:
            msglen = int(msg[:HEADERSIZE])
            new_msg = False

        full_msg += msg

        if len(full_msg) - HEADERSIZE == msglen:
            object = pickle.loads(full_msg[HEADERSIZE:])
            return object


class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "192.168.1.108"
        self.port = 25565
        self.addr = (self.server, self.port)

    def pickle_receive(self):
        return pickle_receive(self.client)

    def pickle_send(self, object):
        pickle_send(self.client, object)

    def communicate(self, msg):
        self.pickle_send(msg)
        return self.pickle_receive()

    def connect(self):
        try:
            self.client.connect(self.addr)
            response = self.pickle_receive()
            self.id = response[0]
            return response[1]

        except Exception as e:
            print(e)