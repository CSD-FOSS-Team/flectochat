
from threading import Thread


class Communication:
    """A basic socket communication wrapper with an internal thread"""

    def __init__(self, socket):
        self.socket = socket
        self.name = socket.getpeername()[0] + ':' + str(socket.getpeername()[1])
        self.live = True
        self.handler = Communication.Handler(self)
        self.handler.start()

    def on_receive(self, message):
        pass

    def on_stop(self):
        pass

    def stop(self):
        self.live = False
        self.socket.close()

    def is_live(self):
        return self.live

    def send(self, message):
        packed = (message + "\n").encode("UTF-8")
        self.socket.send(packed)

    class Handler(Thread):
        """Thread handling a single communication object"""

        def __init__(self, comm):
            super().__init__()
            self.comm = comm

        def run(self):
            data = ""

            while self.comm.live:

                packet = self.comm.socket.recv(1024)

                if len(packet) > 0:
                    data += packet.decode('UTF-8')
                else:
                    break

                while '\n' in data:
                    message, data = data.split('\n', 1)
                    self.comm.on_receive(message)

            self.comm.on_stop()
