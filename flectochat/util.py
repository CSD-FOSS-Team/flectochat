
from time import time


def millis():
    return int(round(time() * 1000))


def tuple_to_address(address):
    return address[0] + ":" + str(address[1])


def address_to_tuple(text):
    parts = text.split(":")
    return parts[0], int(parts[1])


def socket_address(socket):
    return tuple_to_address(socket.getpeername())