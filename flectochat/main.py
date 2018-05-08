
from time import sleep
from threading import Thread
import socket

from flectochat.comm import Communication
from flectochat.util import address_to_tuple, tuple_to_address


class Master(Thread):

    def __init__(self):
        super().__init__()
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # try ports from 8181 to 8199
        for port in range(8181, 8200):
            try:
                s.bind((socket.gethostname(), port))
                break
            except:
                pass

        print("Bound to {0}".format(s))

        self.handler = Handler()
        self.listener = Listener(s, self.handler)

    def run(self):

        self.handler.start()
        self.listener.start()

        while True:

            command = input(">> ")

            if command.startswith("send "):
                _, message = command.split(" ", 1)

                self.handler.send_all(message)

            if command.startswith("connect "):
                _, location = command.split(" ", 1)

                if ":" in location:
                    address = address_to_tuple(location)
                else:
                    address = ("127.0.1.1", int(location))

                if self.handler.has_client(tuple_to_address(address)):
                    print("Already connected")
                else:
                    try:
                        # connect to others
                        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        client.connect(address)
                        print("Listener: Client accepted: {0}".format(client))
                        self.handler.create_client(client)
                    except:
                        print("Failed to connect")

            elif command == "exit":

                self.handler.send_all("bye")

                break
            else:
                pass

        self.listener.stop()
        self.handler.stop()


class Listener(Thread):

    def __init__(self, server_socket, client_handler):
        super().__init__()
        self.live = True
        self.socket = server_socket
        self.handler = client_handler

    def stop(self):
        self.live = False
        self.socket.close()

    def run(self):
        self.socket.settimeout(1)
        self.socket.listen()

        while self.live:

            try:
                client_socket, client_addr = self.socket.accept()
                print("Listener: Client accepted: {0}".format(client_socket))
                self.handler.create_client(client_socket)
            except:
                pass


class Handler(Thread):

    def __init__(self):
        super().__init__()
        self.live = True
        self.clients = []

    def create_client(self, client_socket):
        c = Client(client_socket, self)
        self.clients.append(c)

    def remove_client(self, client):
        self.clients.remove(client)

    def has_client(self, address):
        for i in self.clients:
            if i.name == address:
                return True
        return False

    def send_all(self, message):
        for i in self.clients:
            if i.is_live():
                i.send(message)

    def stop(self):
        self.live = False

    def run(self):
        while self.live:
            sleep(1)

        for i in self.clients:
            if i.is_live():
                i.stop()


class Client(Communication):

    def __init__(self, socket, parent):
        super().__init__(socket)
        self.parent = parent

    def on_receive(self, message):
        print("{0} >> msg >> {1}".format(self.name, message))

    def on_stop(self):
        print("{0} >> end".format(self.name))
        self.parent.remove_client(self)
