import numpy as np
import os

class Node:
    """ Describes a node in a graph, and the edges connected
        to that node."""

    def __init__(self, ID, neighbors, descriptor, truth=None, file_path=None):
        """ Parameters
            ----------
            ID : int
                A unique identifier for this node. Should be a
                value in [0, N-1], if there are N nodes in total.

            neighbors : Sequence[int]
                The node-IDs of the neighbors of this node.

            descriptor : numpy.ndarray
                The (128,) descriptor vector for this node's picture

            truth : Optional[str]
                If you have truth data, for checking your clustering algorithm,
                you can include the label to check your clusters at the end.

                If this node corresponds to a picture of Ryan, this truth
                value can just be "Ryan"

            file_path : Optional[str]
                The file path of the image corresponding to this node, so
                that you can sort the photos after you run your clustering
                algorithm

            """
        self.id = ID

        # The node's label is initialized with the node's ID value at first,
        # this label is then updated during the whispers algorithm
        self.label = ID

        # (n1_ID, n2_ID, ...)
        # The IDs of this nodes neighbors. Empty if no neighbors
        self.neighbors = tuple(neighbors)
        self.descriptor = descriptor

        self.truth = truth
        self.file_path = file_path


    def __repr__():
        return self.id


class Graph:
    """
    """

    def __init__(nodes):
        """

        Parameters
        -----------
        nodes: iterable of nodes
        """
        self.nodes = sorted(nodes)


    def dists(node):
        """

        Parameters
        -----------
        node:
            calculates distances to neighbors of node
        """
        neighbor_descs = [self.nodes[x].descriptor for x in node.neighbors]
        np.array(neighbor_descs, out=neighbor_descs)

        return np.sqrt(np.sum((neighbor_descs - node.descriptor) ** 2))


    def max_neighbor(node):
        """
        Returns label of most common neighbor for given node
        """
        return max([(lab, list(node.neighbors).count(lab)) for lab in unique_labels()], lambda x: x[1])[0]


    def unique_labels():
        """
        Returns set of unique labels
        """
        return set([x.label for x in self.nodes])


    def num_labels():
        """
        Returns number of unique labels in graph
        """
        return len(unique_labels())


    def build_graph():
        """
        """
        prev_labels = num_labels()

        while prev_labels != num_labels():
            rand = np.random.randint(len(self.nodes))
            if len(nodes.neighbors) == 0:
                continue
            elif np.amax(dists(self.nodes[rand])) <= .4:
                self.nodes[rand].label = max_neighbor(self.nodes[rand])
                prev_labels = num_labels()


    def sort_pictures():
        """
        Moves node files to directory and sorts by label
        """
        dirname = os.path.join(os.path.dirname(os.path.realpath(__file__)), "photos")
        if not os.path.exists(dirname):
            os.makedirs(os.path.join(os.path.dirname(os.path.realpath(__file__)), "photos"))

        for node in self.nodes:
            if node.file_path is not None:
                nodedir = os.path.join(dirname, str(node.label))
                if not os.path.exists(nodedir):
                    os.makedirs(nodedir)
                os.rename(node.file_path, os.path.join(nodedir, os.path.split(node.file_path)[1]))
