"""
Class to initialise the parameters such as each nodes, distance and initial pheromone level
"""


class TrailEdges:

    def __init__(self, node_a, node_b, nodes_euclidean_dist, initial_pheromone):
        self.node_a = node_a
        self.node_b = node_b
        self.nodes_euclidean_dist = nodes_euclidean_dist
        self.pheromone = initial_pheromone
