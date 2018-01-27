#!/usr/bin/python3

import os
import time
from random import randint, choice

nb_node = -1


class Node(object):
    """This a class"""
    instances = {}

    def __init__(self, id_number: int, neigh):
        self.id_number = id_number
        self.m = False
        self.p = None
        self.neigh = neigh

    @staticmethod
    def read_graph_file(file_name, mode):
        config_file = open(file_name, mode)
        config_array = config_file.readlines()
        existing_nodes_id = []

        for line in config_array:
            l_split = line.split()

            b = int(l_split[1])

            if "nSommets" in line:
                global nb_node
                nb_node = b
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

    """
    Use to compute pm
    """

    def pm_compute(self):
        for v in self.neigh:
            neigh_j = Node.instances[v]
            if neigh_j.p == self.id_number and self.p == neigh_j.id_number:
                return True
        return False

    # Rule 1
    def check_alliance(self):
        if self.m != self.pm_compute():
            return True
        else:
            return False

    def alliance(self, m):
        self.m = m
        self.print_state(0, "Alliance")

    # Rule 2
    def check_wedding(self):
        if self.m == self.pm_compute() and self.p == None:
            for jNeigh in self.neigh:
                neighbour = Node.instances[jNeigh]
                if neighbour.p == self.id_number:
                    return (True, neighbour.id_number)

        return (False, None)

    def wedding(self, id_number):
        self.p = id_number
        self.print_state(0, "Mariage")

    # Rule 3
    def check_seduction(self):
        if self.m == self.pm_compute() and self.p is None:
            for k in self.neigh:
                neighbour = Node.instances[k]
                if neighbour.p == self.id_number:
                    return (False, None)

            max = -1
            for j in self.neigh:
                neighbour = Node.instances[j]
                if neighbour.p is None and neighbour.id_number > self.id_number and not neighbour.m:
                    max = neighbour.id_number
            if max != -1:
                return (True, max)
            else:
                return (False, None)

        return (False, None)

    def seduction(self, id_number):
        self.p = id_number
        self.print_state(0, "Séduction")

    # Rule 4
    def check_divorse(self):
        if self.p is not None:
            j = Node.instances[self.p]
            if self.m == self.pm_compute() and self.p is not None and j.p != self.id_number and (
                    j.m or j.id_number <= self.id_number):
                return True

        return False

    def divorce(self):
        self.p = None
        self.print_state(0, "Divorce")

    def print_state(self, nb_tab=0, typeOperation=""):
        """printState node state"""
        for i in range(nb_tab):
            print("\t", end='')
        print("id: " + str(self.id_number) + ", M: " + str(self.m) + ", P: " + str(self.p) + ", Neigh: " + str(
            self.neigh) + "\t" + typeOperation)

    def update(self):
        """
            update val of a node
        """

        if self.check_alliance():
            self.alliance(True)
            return True

        (res, node_id) = self.check_wedding()
        if res:
            self.wedding(node_id)
            return True

        yolo = self.check_seduction()
        print(yolo)
        (res, node_id) = yolo

        if res:
            self.seduction(node_id)
            return True

        if self.check_divorse():
            self.divorce()
            return True

        return False


def initlist():
    list_nodes = []
    for node in Node.instances.values():
        list_nodes.append(node)
    return list_nodes


if __name__ == '__main__':
    dir_path = os.path.dirname(os.path.realpath(__file__))
    # Read and make graph structure
    Node.read_graph_file(dir_path + '/graphe_config.txt', 'r')

    print("============ Initial configurations ============")
    for node in Node.instances.values():
        node.print_state()
    print("================================================")

    list_nodes = initlist()
    while len(list_nodes) > 0:
        node = choice(list_nodes)
        res = node.update()
        if res:
            list_nodes = initlist()
        else:
            list_nodes.remove(node)

    for node in Node.instances.values():
        node.print_state()
