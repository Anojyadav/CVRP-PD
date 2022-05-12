import math
from TrailEdges import TrailEdges
from AntColony import AntColony


class AntTour:

    def __init__(self, colony_size=5, alpha=1.0, beta=3.0, rho=0.1, pheromone_deposit_weight=1.0,
                 initial_pheromone=1.0, steps=50, nodes_location=None,
                 labels=None, demand_list=None, robot_capacity=10, pick_drop_list=None):

        self.colony_size = colony_size
        self.rho = rho
        self.pheromone_deposit_weight = pheromone_deposit_weight
        self.steps = steps
        self.total_nodes = len(nodes_location)
        self.nodes_location = nodes_location
        self.robot_capacity = robot_capacity
        self.nodes_demand_list = demand_list
        self.pick_drop_list = pick_drop_list

        if labels is not None:
            self.labels = labels
        else:
            self.labels = range(1, self.total_nodes + 1)
        self.trail = [[None] * self.total_nodes for _ in range(self.total_nodes)]
        for i in range(self.total_nodes):
            for j in range(i + 1, self.total_nodes):
                self.trail[i][j] = self.trail[j][i] = TrailEdges(i, j, math.sqrt(
                    pow(self.nodes_location[i][0] - self.nodes_location[j][0], 2.0) + pow(
                        self.nodes_location[i][1] - self.nodes_location[j][1], 2.0)), initial_pheromone)

        self.ants = [AntColony(alpha, beta, self.total_nodes, self.trail, self.nodes_demand_list, self.robot_capacity,
                               self.pick_drop_list) for _ in range(self.colony_size)]
        self.global_best_tour = [0]
        self.global_best_distance = float("inf")

    def add_phermone(self, tour, distance, weight=1.0):

        pheromone_to_add = self.pheromone_deposit_weight / distance
        for i in range(len(tour)):
            self.trail[tour[i]][tour[(i + 1) % len(tour)]].pheromone += weight * pheromone_to_add

    def aco(self):

        for step in range(self.steps):
            for ant in self.ants:
                self.add_phermone(ant.find_tour(), ant.get_distance())
                if ant.distance < self.global_best_distance:
                    self.global_best_tour = ant.tour
                    self.global_best_distance = ant.distance

            for i in range(self.total_nodes):
                for j in range(i + 1, self.total_nodes):
                    self.trail[i][j].pheromone *= (1.0 - self.rho)

    def run(self):

        self.aco()
        station_list = [self.nodes_location[int(str(self.labels[j])) - 1] for j in self.global_best_tour]
        return self.global_best_tour, station_list, self.global_best_distance
