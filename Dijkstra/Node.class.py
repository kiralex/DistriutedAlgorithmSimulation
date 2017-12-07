#!/usr/bin/python3

from random import randint
import time

NB = 4

class Node(object):
  """This a class"""
  instances = []

  def __init__(self, id_number, initVal):
    self.id_number = id_number
    self.val = initVal


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
