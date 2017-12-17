#!/usr/bin/python3

import os
import time
from random import randint

nb_node = -1


class Node(object):
    """This a class"""
    instances = {}

    def __init__(self, id_number: int, neigh):
        self.id_number = id_number
        self.m = False
        self.p = None
        self.neigh = neigh

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
    def alliance(self):
        if self.m != self.pm_compute():
            self.m = self.pm_compute()
            self.print_state()
            print("--------------------------------------------\n")

    # Rule 2
    def wedding(self):
        if self.m == self.pm_compute() and self.p == None:
            for jNeigh in self.neigh:
                neighbour = Node.instances[jNeigh]
                if neighbour.p == self.id_number:
                    self.p = neighbour.id_number
                    self.print_state()
                    print("--------------------------------------------\n")
                    return

    # Rule 3
    def seduction(self):
        if self.m == self.pm_compute() and self.p is None:
            for k in self.neigh:
                neighbour = Node.instances[k]
                if neighbour.p == self.id_number:
                    return
            for j in self.neigh:
                neighbour = Node.instances[j]
                if neighbour.p is None and neighbour.id_number > self.id_number and not neighbour.m:
                    self.p = self.max_seduction()
                    self.print_state()
                    print("--------------------------------------------\n")
                    return

    # Rule 3 bis
    def max_seduction(self):
        max = 0
        for j in self.neigh:
            neighbour = Node.instances[j]
            if neighbour.p is None and neighbour.id_number > self.id_number and not neighbour.m:
                if neighbour.id_number > max:
                    max = neighbour.id_number
        return max

    # Rule 4
    def divorce(self):
        if self.p is not None:
            j = Node.instances[self.p]
            if self.m == self.pm_compute() and self.p is not None and j.p != self.id_number and (
                j.m or j.id_number <= self.id_number):
                self.p = None
                self.print_state()
                print("--------------------------------------------\n")

    def get_val(self):
        """get val of a node"""
        return self.val

    def print_state(self, nb_tab=0):
        """printState node state"""
        for i in range(nb_tab):
            print("\t", end='')
        print("id: " + str(self.id_number) + ", M: " + str(self.m) + ", P: " + str(self.p) + ", Neigh: " + str(
            self.neigh))

    def update(self):
        """
            update val of a node
        """
        continue_update = Node.continue_loop()
        if continue_update:
            selected_rule = randint(1, 4)
            print("node id : " + str(self.id_number) + " | rule id : " + str(selected_rule), end='')
            if selected_rule == 1:
                print(" ==> Alliance")
                self.alliance()
            elif selected_rule == 2:
                print(" ==> Wedding")
                self.wedding()
            elif selected_rule == 3:
                print(" ==> Seduction")
                self.seduction()
            else:
                print(" ==> Divorce")
                self.divorce()
            print()
        return continue_update

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
                    print(a)
                    print(b)
                    Node.instances[b].neigh.append(a)

    @staticmethod
    def continue_loop():
        """"
            :return false if nb Node with M properties at "True" is >= nb_node-1
            :return true otherwise

        """
        count = 0
        for node_v in Node.instances.values():
            if node_v.m:
                count += 1
        if nb_node%2 == 0: # even number
            res = (count < len (Node.instances))
        else: # not even number
            res = (count < len(Node.instances) - 1)
        return res


if __name__ == '__main__':
    continue_loop = True
    count_loop = 0
    dir_path = os.path.dirname(os.path.realpath(__file__))
    # Read and make graph structure
    Node.read_graph_file(dir_path + '/graphe_config.txt', 'r')

    print("===== Graph Begin configuration ====================")
    for node in Node.instances.values():
        node.print_state()
    print("==============================================\n")

    print("---- Execution -------------------------------\n")
    while continue_loop and count_loop < 10000:
        if count_loop%1000 == 0:
            print("===== Graph " + str(count_loop) + " iterate configuration ====================")
            for node in Node.instances.values():
                node.print_state()
            print("==============================================\n")

        ID = randint(1, nb_node)
        continue_loop = Node.instances[ID].update()
        count_loop += 1
        # time.sleep(0.005)


    print("===== Graph Final configuration ====================")
    for node in Node.instances.values():
        node.print_state()
