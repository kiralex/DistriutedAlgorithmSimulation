#!/usr/bin/python3

from random import randint
import time


NB = 4

class Node(object):
    """This a class"""
    instances = []


    def __init__(self, id_number, initVal, neigh):
        self.id_number = id_number
        self.val = initVal
        self.m = False
        self.p = None
        self.neigh = neigh

    """
    Use to compute pm
    """
    def pmCompute (self):
        for v in self.neigh:
            neighJ = Node.instances[v]
            if neighJ.p == self.id_number and self.p == neighJ.id_number:
                return True
        return False



    # Rule 1
    def alliance (self):
        print ("r")
        if self.m != self.pmCompute():
            self.m = self.pmCompute()

    # Rule 2
    def wedding (self):
        if self.m == self.pmCompute() and self.p == None:
            for jNeigh in self.neigh:
                neighbour = Node.neigh[jNeigh]
                if neighbour.p == self.id_number:
                    self.p = neighbour.id_number
                    return
    # Rule 3
    def seduction (self):
        if self.m == self.pmCompute() and self.p == None:
            for k in self.neigh:
                neighbour = Node.neigh[k]
                if neighbour.p == self.id_number:
                    return
            for j in self.neigh:
                neighbour = Node.neigh[k]
                if neighbour.p == None and neighbour.id_number > self.id_number and not neighbour.m:
                    self.p = self.max_seduction()

    # Rule 3 bis
    def max_seduction (self):
        max = 0
        for j in self.neigh:
            neighbour = Node.neigh[j]
            if neighbour.p == None and neighbour.id_number > self.id_number and not neighbour.m:
                if (neighbour.id_number > max):
                    max = neighbour.id_number
        return max

    # Rule 4
    def divorce (self):
        j = Node.neigh[self.p]
        if self.m == self.pmCompute() and self.p != None and j.p != self.id_number and (j.m or j.id_number <= self.id_number):
            self.p = None


    def get_val(self):
        """get val of a node"""
        return self.val

    def printState(self, nbTab=0):
        """printState node state"""
        for i in range(nbTab):
            print("\t", end='')
        print("id: " + str(self.id_number) + ", val: " + str(self.val))


    def update(self):
        """update val of a node"""

        prev_val = Node.instances[(self.id_number - 1) % NB].get_val()

        if self.id_number > 0 and prev_val != self.val:
            self.val = prev_val
            self.printState(3)
            print()
        if self.id_number == 0 and prev_val == self.val:
            self.val = (self.val + 1) % NB
            self.printState(3)
            print()


if __name__ == '__main__':
    print("initial values : ")
    for i in range(0, NB):
        mytest = Node(i, randint(0, NB - 1))
        Node.instances.append(mytest)
        mytest.printState()

    print("=========================\n")

    while True:
        ID = randint(0, NB-1)
        print("random selected id : " + str(ID))
        Node.instances[ID].update()
        time.sleep(1)
