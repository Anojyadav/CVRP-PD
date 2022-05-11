import random
import copy

'''
Ant Colony class to build tour for each ant in the ant colony using heuristics
'''


class AntColony:

    def __init__(self, alpha, beta, total_nodes, trail, nodes_demand_list, robot_capacity, pick_drop_list):

        self.alpha = alpha
        self.beta = beta
        self.total_nodes = total_nodes
        self.trail = trail
        self.tour = None
        self.nodes_demand_list = nodes_demand_list
        self.robot_capacity = robot_capacity
        self.pick_drop_list = pick_drop_list
        self.demand_list_ = copy.deepcopy(nodes_demand_list)
        self.distance = 0.0

    def node(self):

        roulette_wheel = 0.0
        new_nodes = [node for node in range(self.total_nodes) if node not in self.tour]
        heuristic_total = 0.0
        for new_node in new_nodes:
            heuristic_total += self.calculate_heuristic_value(new_node)

        for new_node in new_nodes:
            roulette_wheel += self.probability_func(new_node, heuristic_total)

        random_value = random.uniform(0, roulette_wheel)
        wheel_position = 0.0
        for new_node in new_nodes:
            wheel_position += self.probability_func(new_node, heuristic_total)
            if wheel_position >= random_value:
                for i_ in range(len(self.pick_drop_list)):
                    if new_node in self.pick_drop_list[i_]['pick_drop'][:-1]:
                        a_ = self.check_demand(self.pick_drop_list[i_]['pick_drop'][:-1])
                        if a_ <= self.tour_capacity:
                            self.tour_capacity = self.tour_capacity - a_
                            self.set_visited_node(self.pick_drop_list[i_]['pick_drop'][:-1])
                            self.nodes_demand_list[new_node] = float('inf')
                            return new_node

                    elif self.pick_drop_list[i_]['pick_drop'][-1] == new_node and all(elem in self.tour for elem in
                                                                                      self.pick_drop_list[i_][
                                                                                          'pick_drop'][
                                                                                      :-1]):  # self.pick_drop_list[i_][:-1] in self.tour :
                        return new_node

    def calculate_heuristic_value(self, node_):

        return self.trail[self.tour[-1]][node_].nodes_euclidean_dist

    def probability_func(self, node_, heuristic_value):

        amount_of_pheromone = pow(self.trail[self.tour[-1]][node_].pheromone, self.alpha)
        desirability_arc = pow((heuristic_value / self.trail[self.tour[-1]][node_].nodes_euclidean_dist), self.beta)
        return amount_of_pheromone * desirability_arc

    def check_demand(self, a):

        node_demand = 0
        list_ = []
        for j_ in a:
            list_.append(self.nodes_demand_list[j_])
        if min(list_) == float('inf'):
            node_demand = float('inf')
            return node_demand
        elif min(list_) != float('inf'):
            for i_ in a:
                if self.nodes_demand_list[i_] != float('inf'):
                    node_demand += self.nodes_demand_list[i_]
            return node_demand

    def set_visited_node(self, k):

        for l_ in k:
            if self.nodes_demand_list[l_] != float('inf'):
                self.nodes_demand_list[l_] = 0.0

    def check_pd(self):

        check_list = []
        for j_ in self.tour[1:]:
            for i_ in range(len(self.pick_drop_list)):
                if j_ in self.pick_drop_list[i_]['pick_drop'][:-1] and all(
                        elem in self.tour for elem in self.pick_drop_list[i_]['pick_drop']):
                    check_list.append(0)
                elif j_ in self.pick_drop_list[i_]['pick_drop'][:-1] and (
                        all(elem in self.tour for elem in self.pick_drop_list[i_]['pick_drop']) is False):
                    check_list.append(-1)
        if min(check_list) == 0:
            return 1
        elif min(check_list) == -1:
            return 0

    def check_min(self):

        check_min_list = []
        for a in range(len(self.pick_drop_list)):
            demand_tour = 0
            for j_ in self.pick_drop_list[a]['pick_drop'][:-1]:
                demand_tour += self.nodes_demand_list[j_]
            check_min_list.append(demand_tour)
        return min(check_min_list)

    def find_tour(self):

        self.tour_capacity = self.robot_capacity
        self.tour = [0]
        self.nodes_demand_list = copy.deepcopy(self.demand_list_)
        self.nodes_demand_list[0] = float('inf')
        while True:
            city_node = self.node()
            if city_node is not None:
                self.tour.append(city_node)

            elif self.tour_capacity <= self.check_min() and self.check_pd() == 1:
                break

        return self.tour

    def get_distance(self):

        self.distance = 0.0
        for i in range(len(self.tour)):
            self.distance += self.trail[self.tour[i]][self.tour[(i + 1) % len(self.tour)]].nodes_euclidean_dist
        return self.distance
