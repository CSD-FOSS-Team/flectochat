
from time import sleep
from threading import Thread
import socket


class Listener(Thread):

    def __init__(self, server_socket, client_handler):
        super().__init__(daemon=True)
        self.socket = server_socket
        self.handler = client_handler

    def run(self):
        self.socket.listen()

        while True:

            client_socket, client_addr = self.socket.accept()
            print("Listener: Client accepted: {0}".format(client_socket))
            self.handler.create_client(client_socket)
            sleep(1)


class Handler(Thread):

    def __init__(self):
        super().__init__()
        self.clients = []

    def create_client(self, client_socket):
        c = Client(client_socket, self)
        c.start()
        self.clients.append(c)

    def remove_client(self, client):
        self.clients.remove(client)

    def run(self):
        while True:

            sleep(1)


class Client(Thread):

    def __init__(self, socket, handler):
        super().__init__(daemon=True)
        self.socket = socket
        self.handler = handler
        self.name = socket.getpeername()[0] + ':' + str(socket.getpeername()[1])

    def run(self):
        data = ""

        while True:

            packet = self.socket.recv(1024)

            if len(packet) > 0:
                data += packet.decode('UTF-8')
            else:
                break

            while '\n' in data:
                message, data = data.split('\n', 1)
                print("{0} >> msg >> {1}".format(self.name, message))

        print("{0} >> end".format(self.name))
        handler.remove_client(self)


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((socket.gethostname(), 8181))

handler = Handler()
listener = Listener(s, handler)

handler.start()
listener.start()

input("")
s.close()
print("The end")
