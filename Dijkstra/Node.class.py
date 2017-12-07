#!/usr/bin/python3


class Node(object):
    def __init__(self, id, initVal):
        self.id = id
        self.val = initVal

    def print(self):
        print self.id
