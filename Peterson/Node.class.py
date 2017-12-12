#!/usr/bin/python3

import logging
import pickle
import time
import sys
import traceback
import signal
from struct import pack, unpack
from threading import Lock, Thread
from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR
import coloredlogs
import zmq

#  to color error and debug output
coloredlogs.install()

NB = 10
ACTIVE = "a"
PASSIVE = "p"
LEADER = "l"
BEATEN = "b"

ONE = 1
TWO = 2
SMALL = 3


class Node(Thread):
    """This a class"""
    instances = []
    nbConnectedLock = Lock()
    nbConnected = 0


    def __init__(self, id_number, candidate):
        Thread.__init__(self)

        # peterson variables
        self.id_number = id_number
        self.c = self.id_number
        self.acn = None
        self.win = None
        self.state = None
        self.candidate = candidate
        
        self.server_port = 20000 + id_number
        self.client_port = 20000 + ((self.id_number + 1) % NB)

        context = zmq.Context()
        self.server_socket = context.socket(zmq.PAIR)
        self.socket_client = context.socket(zmq.PAIR)
        self.server_socket.bind("tcp://*:%s" % str(self.server_port))
        self.socket_client.connect("tcp://127.0.0.1:%s" %
                                   str(self.client_port))


    def send(self, data):
        print(str(self.id_number) + " : j'envoi " + str(data))
        packet = pickle.dumps(data)
        self.socket_client.send(packet)

    def receive(self, message_type=None):
        print(str(self.id_number) + " : j'attends " + str(message_type))

        data = self.server_socket.recv(4096)
        data = pickle.loads(data)
        if message_type != None and data["type"] != message_type:
            raise Exception("Message innatendu: " + str(data))

        return data

    def run(self):
        if self.candidate:
            self.state = ACTIVE
        else:
            self.state = PASSIVE

        while self.win is None:
            if self.state == ACTIVE:
                self.send({"type": ONE, "val": self.c})
                data = self.receive(ONE)

                self.acn = data["val"]
                if self.acn == self.c:
                    self.send({"type": SMALL, "val": self.c})
                    data = self.receive(SMALL)
                    self.win = data["val"]
                else:
                    self.send({"type": TWO, "val": self.acn})
                    data = self.receive(TWO)
                    if self.acn < self.c and self.acn < data["val"]:
                        self.c = self.acn
                    else:
                        self.state = PASSIVE
                        print(str(self.id_number) + " devient passif")
            else:
                data = self.receive(ONE)
                self.send({"type": ONE, "val": data["val"]})
                data = self.receive()
                self.send(data)
                if data["type"] == SMALL:
                    self.win = data["val"]

        if self.id_number == self.win:
            print("je suis " + str(self.id_number) + " : je gagne")
            self.state = LEADER
        else:
            print("je suis " + str(self.id_number) + ": je perd")
            self.state = BEATEN


def main():
    for i in range(NB):
        Node.instances.append(Node(i, True))

    for i in range(NB):
        Node.instances[i].start()

    for i in range(NB):
        Node.instances[i].join()


main()
