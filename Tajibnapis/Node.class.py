#!/usr/bin/python3

import os
from termcolor import colored, cprint
import pprint

# Create a logger object.
pp = pprint.PrettyPrinter(indent=8, width=60)

NB_NODE = 0


class Node(object):
    """This a class"""
    instances = {}

    def __init__(self, id_number: int, neigh):
        self.id_number = id_number
        self.neigh = neigh

        self.evts = []
        self.d = {}
        self.nb = {}
        self.nDis = {}

    def initialize(self):
        for w in self.neigh:
            self.nDis[w] = {}

        for w in self.neigh:
            for v in range(1, NB_NODE+1):
                self.nDis[w][v] = NB_NODE

        for v in range(1, NB_NODE+1):
            self.d[v] = NB_NODE
            self.nb[v] = None

        self.d[self.id_number] = 0
        self.nb[self.id_number] = "local"

        for w in self.neigh:
            self.send(w, {"type": "myDist", "v": self.id_number,
                          "d": 0, "w": self.id_number})

    def printState(self):
        print("id:\t%d" % self.id_number)
        print("d:\t%s" % self.d)
        print("nb:\t%s" % self.nb)
        print("nDis:")
        pp.pprint(self.nDis)
        print()

    def send(self, dest, msg):
        Node.instances[dest].evts.append(msg)
        cprint(str(self.id_number) + " -> " +
               str(dest) + ": \t " + str(msg), "green")

    def recv(self):
        if len(self.evts) == 0:
            return False

        msg = self.evts.pop(0)
        if msg["type"] == "myDist":
            return self.myDist(msg)

    def myDist(self, msg):
        self.nDis[msg["w"]][msg["v"]] = msg["d"]
        return self.recompute(msg["v"])

    def recompute(self, v):
        old_dv = self.d[v]

        if v == self.id_number:
            self.d[v] = 0
            self.nb[v] = "local"
            return False
        else:
            mini = NB_NODE
            vois = None

            for k in self.neigh:
                if self.nDis[k][v] < mini:
                    mini = self.nDis[k][v]
                    vois = k

            # for key, val in self.nDis.items():
            #     if val[v] < mini:
            #         mini = val[v]
            #         vois = key
            d = 1+mini

            if d < NB_NODE:
                self.d[v] = d
                self.nb[v] = vois
            else:
                self.d[v] = NB_NODE
                self.nb[v] = None

        if old_dv != self.d[v]:
            for x in self.neigh:
                self.send(x, {"type": "myDist", "v": v,
                              "d": self.d[v], "w": self.id_number})
            return True

        return False

    def fail(self, w):
        if w in self.neigh:
            self.neigh.remove(w)
            for v in range(1, NB_NODE+1):
                self.recompute(v)

    def repair(self, w):
        self.neigh.append(w)
        for v in range(1, NB_NODE+1):
            self.nDis[w][v] = NB_NODE
            self.send(w, {"type": "myDist", "v": v,
                          "d": self.d[v], "w": self.id_number})


    @staticmethod
    def read_graph_file(file_name, mode):
        config_file = open(file_name, mode)
        config_array = config_file.readlines()
        existing_nodes_id = []

        for line in config_array:
            l_split = line.split()

            b = int(l_split[1])

            if "nSommets" in line:
                global NB_NODE
                NB_NODE = b
            else:
                a = int(l_split[0])
                # Add node 1
                if a not in existing_nodes_id:
                    node = Node(a, [b])
                    Node.instances[a] = node
                    existing_nodes_id.append(a)
                else:
                    Node.instances[a].neigh.append(b)

                # Add node 2
                if b not in existing_nodes_id:
                    node = Node(b, [a])
                    Node.instances[b] = node
                    existing_nodes_id.append(b)
                else:
                    Node.instances[b].neigh.append(a)

    @staticmethod
    def max_nb_events():
        maxi = 0
        for k, v in Node.instances.items():
            if len(v.evts) > maxi:
                maxi = len(v.evts)

        return maxi

    def loop_all_events():
        while Node.max_nb_events() > 0:
            msg_env = False
            for k, node in Node.instances.items():
                if node.recv() and not msg_env:
                    msg_env = True

            if msg_env:
                print()

        print("==============================================\n")


def main():

    dir_path = os.path.dirname(os.path.realpath(__file__))
    # Read and make graph structure
    Node.read_graph_file(dir_path + '/graphe_config5.txt', 'r')

    for k, node in Node.instances.items():
        node.initialize()
    print()
    
    Node.loop_all_events()


    for k, node in sorted(Node.instances.items()):
        node.printState()
        
    Node.instances[1].fail(3)
    Node.instances[3].fail(1)
    Node.loop_all_events()
    
    for k, node in sorted(Node.instances.items()):
        node.printState()

    Node.instances[1].repair(3)
    Node.instances[3].repair(1)
    Node.loop_all_events()

    for k, node in sorted(Node.instances.items()):
        node.printState()


main()
