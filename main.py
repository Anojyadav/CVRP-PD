from GenerateOrderList import GenerateOrderList
from AntTour import AntTour
import copy
import math
import random


class CapacityVehicleRoutingPickupDelivery(GenerateOrderList):

    def __init__(self, colony_size, steps, robot_parameters):
        super().__init__()
        self.colony_size = colony_size
        self.steps = steps
        self.robot_parameters = robot_parameters
        self.robot_name_list = None
        self.total_distance_travelled = 0.0
        self.best_tour = [0]
        self.best_distance = float("inf")
        self.best_robot_parameters = [0]
        self.tour_nodes = [0]
        self.nodes_location = []

    def sort_in(self):

        self.robot_parameters.sort(key=lambda x: x['Capacity'], reverse=True)

    def check_unvisited(self, a, c, mode):

        k = []
        for s in c:
            if all(elem in a for elem in s['pick_drop']):
                continue
            else:
                if mode == 'demand':
                    k.append(s['total_demand_tour'])
                if mode == 'unvisited_nodes':
                    k.append(s)
        return k

    def random_shuffle_(self):

        robot_list = []
        while True:
            robot_parameters_ = copy.deepcopy(self.robot_parameters)
            n = len(robot_list)
            if n >= math.factorial(len(robot_parameters_)):
                break
            else:
                random.shuffle(robot_parameters_)
                if robot_parameters_ not in robot_list:
                    robot_list.append(robot_parameters_)
        return robot_list

    def tour_(self, robot_list, demand, pick_drop_list):

        total_distance = 0
        tour_list = []
        tour_nodes = []
        for robot in range(len(robot_list)):

            unvisited_node_demand = self.check_unvisited(tour_nodes, pick_drop_list, mode='demand')
            if len(unvisited_node_demand) == 0:
                break
            elif robot_list[robot]['Capacity'] < min(unvisited_node_demand):
                tour_list.append(None)
                continue
            else:

                tour = AntTour(colony_size=self.colony_size, steps=self.steps, nodes_location=self.nodes_location,
                               demand_list=demand, robot_capacity=robot_list[robot]['Capacity'],
                               pick_drop_list=pick_drop_list)
                a, c, d = tour.run()
                total_distance += round(d, 2)
                tour_list.append(a)
                tour_nodes.extend(a)
                for ele in a:
                    if ele != 0:
                        demand[ele] = float('inf')
                if min(demand[1:]) == float('inf'):
                    break

        return total_distance, tour_list, tour_nodes

    def main(self, mode='Sorting'):

        self.nodes_location, demand_list, pick_drop_list = self.generate_order_list()
        if mode != 'Sorting':
            robot_parameter_list = self.random_shuffle_()
            self.task_optimization_shuffle(demand_list, robot_parameter_list, pick_drop_list)
        else:
            self.sort_in()
            self.task_optimization_sorting(demand_list, pick_drop_list)

    def task_optimization_sorting(self, demand_list, pick_drop_list):

        self.best_distance, self.best_tour, self.tour_nodes = self.tour_(self.robot_parameters, demand_list, pick_drop_list)
        unvisted_nodes = self.check_unvisited(self.tour_nodes, pick_drop_list, mode='unvisited_nodes')
        self.print_results(unvisted_nodes,self.robot_parameters)
        if len(unvisted_nodes) != 0:
            self.task_optimization_sorting(demand_list, unvisted_nodes)
        else:
            return

    def task_optimization_shuffle(self, demand_list, robot_parameter_list, pick_drop_list):

        for robot_list in robot_parameter_list:
            demand_list_ = copy.deepcopy(demand_list)
            total_distance, tour_list, tour_nodes = self.tour_(robot_list, demand_list_, pick_drop_list)

            if total_distance < self.best_distance:
                self.best_tour = tour_list
                self.best_distance = round(total_distance, 3)
                self.best_robot_parameters = robot_list
                self.tour_nodes = tour_nodes

        unvisted_nodes = self.check_unvisited(self.tour_nodes, pick_drop_list, mode='unvisited_nodes')
        self.print_results(unvisted_nodes,self.best_robot_parameters)
        if len(unvisted_nodes) != 0:
            self.task_optimization_shuffle(demand_list, robot_parameter_list, unvisted_nodes)
        else:
            return

    def print_results(self,unvisted_nodes,robot_seq):

        print("total distance traveled {}".format(self.best_distance))
        print("best robot sequence parameter {}".format(robot_seq))
        print("best tour for all robot based on seq {}".format(self.best_tour))
        print("unvisited_nodes by the robots {}".format(unvisted_nodes))


if __name__ == '__main__':
    colony_size = 5
    steps = 50
    robot_parameters = [{'name': 'Captain', 'Capacity': 10}, {'name': 'Cob', 'Capacity': 30},
                        {'name': 'Davy', 'Capacity': 30}]
    cvrp = CapacityVehicleRoutingPickupDelivery(colony_size, steps, robot_parameters)
    cvrp.main(mode='Shuffle')

