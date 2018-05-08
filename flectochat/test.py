

from time import sleep
from threading import Thread
import socket


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((socket.gethostname(), 8181))

print(s.getpeername()[0] + ':' + str(s.getpeername()[1]))

def send(s, raw, end="\n"):
    message = (raw + end).encode("UTF-8")
    s.send(message)


while True:
    raw_message = input(">> ")

    if len(raw_message) == 0:
        break

    send(s, raw_message)

s.close()