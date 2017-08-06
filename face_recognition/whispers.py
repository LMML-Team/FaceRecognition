import numpy as np
import os
from itertools import groupby

class Node:
    """ Describes a node in a graph, and the edges connected
        to that node."""

    def __init__(self, ID, descriptor, truth=None, file_path=None):
        """
        Parameters
        ----------
        ID : int
            a unique identifier for this node. Should be a
            value in [0, N-1], if there are N nodes in total.

        descriptor : numpy.ndarray
            The (128,) descriptor vector for this node's picture

        truth : Optional[str]
            if you have truth data, for checking your clustering algorithm,
            you can include the label to check your clusters at the end.

            if this node corresponds to a picture of Ryan, this truth
            value can just be "Ryan"

        file_path : Optional[str]
            the file path of the image corresponding to this node, so
            that you can sort the photos after you run your clustering
            algorithm

            """
        self.id = ID

        # The node's label is initialized with the node's ID value at first,
        # this label is then updated during the whispers algorithm
        self.label = ID

        # (n1_ID, n2_ID, ...)
        # The IDs of this nodes neighbors. Empty if no neighbors
        self.neighbors = None
        self.descriptor = descriptor

        self.truth = truth
        self.file_path = file_path


    def __repr__(self):
        return str(self.id)


    def __eq__(self, y):
        return self.label == y


    def __ne__(self, y):
        return self.label != y


    def __lt__(self, y):
        return self.label < y


    def __le__(self, y):
        return self.label <= y


    def __gt__(self, y):
        return self.label > y


    def __ge__(self, y):
        return self.label >= y


class Graph:
    """
    Graph of Nodes for runnng whispers algorithm
    """

    def __init__(self, nodes, directory=None):
        """
        Parameters
        -----------
        nodes: list of Nodes
            Nodes to be included in graph
        directory: r"PATH"
            path to directory for photos to be sorted
        """
        self.nodes = sorted(nodes)
        self.directory = directory


    def set_all_neighbors(self):
        """
        Determines and sets all neighbors of nodes in graph
        """
        for node in self.nodes:
            dists = self.dists(node, self.nodes)
            dists = np.where((dists <= .4) & (dists != 0))[0]
            node.neighbors = tuple(self.nodes[x] for x in dists)


    def dists(self, node, nodes):
        """
        Determines distance between node and all Nodes in nodes

        Parameters
        -----------
        node:
            calculates distances to neighbors of node
        nodes:
            iterable of nodes to calculate distances from
        """
        descs = np.vstack((x.descriptor for x in nodes))
        return np.sqrt(np.sum((descs - node.descriptor) ** 2, axis=1))


    def max_neighbor(self, node):
        """
        Returns label of most common neighbor for given node

        Parameters
        -----------
        node: Node
            node to find most common neighbor of
        """
        return max([(lab, node.neighbors.count(lab)) for lab in self.unique_labels()], key=lambda x: x[1])[0]


    def unique_labels(self):
        """
        Returns set of unique labels
        """
        return set([x.label for x in self.nodes])


    def num_labels(self):
        """
        Returns number of unique labels in graph
        """
        return len(self.unique_labels())


    def build_graph(self):
        """
        Builds graph of nodes and performs whispers algorithm
        """
        prev_labels = [0, 1, 2, 3]

        while prev_labels[::1] != prev_labels[::-1]:
            rand = np.random.randint(len(self.nodes))
            if len(self.nodes[rand].neighbors) == 0:
                continue
            elif np.amax(self.dists(self.nodes[rand], self.nodes[rand].neighbors)) <= .4:
                prev_labels[0] = prev_labels[1]
                prev_labels[1] = prev_labels[2]
                prev_labels[2] = prev_labels[3]
                prev_labels[3] = self.num_labels()
                self.nodes[rand].label = self.max_neighbor(self.nodes[rand])


    def sort_pictures(self):
        """
        Moves node files to directory and sorts by label
        """
        # creates new directory for photos if none provided in Graph initialiation
        if self.directory is None:
            dirname = os.path.join(os.path.dirname(os.path.realpath(__file__)), "photos")
            if not os.path.exists(dirname):
                os.makedirs(os.path.join(os.path.dirname(os.path.realpath(__file__)), "photos"))
        else:
            dirname = self.directory

        # determines most common truth value in clusters
        truth_dict = {}
        for node in self.nodes:
            if node.truth is not None:
                if str(node.label) not in truth_dict:
                    truth_dict[str(node.label)] = [node.truth]
                else:
                    truth_dict[str(node.label)].append(node.truth)
        for lab in truth_dict:
            truth_dict[lab] = max([list(g) for k, g in groupby(sorted(ls))], key=lambda x: len(x))[0]

        # saves image associated with node to directory named either label or truth value
        for node in self.nodes:
            if node.file_path is not None:
                if node.label in truth_dict:
                    nodedir = os.path.join(dirname, truth_dict[node.label])
                else:
                    nodedir = os.path.join(dirname, str(node.label))
                if not os.path.exists(nodedir):
                    os.makedirs(nodedir)
                os.rename(node.file_path, os.path.join(nodedir, os.path.split(node.file_path)[1]))
