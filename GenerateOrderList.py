import yaml

'''
class to generate the order list and all the parameters related to the order
'''


class GenerateOrderList:

    def __init__(self):
        self.total_nodes = 0
        self.demand_list = []
        self.nodes_location = []
        self.pick_drop_list = []
        file_location = "Order_2.yaml"
        with open(file_location, 'r') as f:
            self.order_dict = yaml.safe_load(f)

    def generate_order_list(self):

        deposit_ = []
        delivery_node_ = []
        idxx_list = []
        self.total_nodes = len(self.order_dict)
        for idxx, station in enumerate(self.order_dict.values()):
            self.nodes_location.append([station['position'].get('x'), station['position'].get('y')])
            self.demand_list.append(station['demand'])
            deposit_.append(station['deposit'])
            if station['type'] == 'drop_loc':
                delivery_node_.append(station['name'])
                idxx_list.append(idxx)

        for j_ in range(len(delivery_node_)):
            pick_up_list = []
            total_demand_tour = 0
            pick_up_list.append(idxx_list[j_])
            for count, k_ in enumerate(deposit_):
                if k_ == delivery_node_[j_]:
                    pick_up_list.insert(0, count)
                    total_demand_tour += self.demand_list[count]
            self.pick_drop_list.append({'pick_drop': pick_up_list, 'total_demand_tour': total_demand_tour})

        return self.nodes_location, self.demand_list, self.pick_drop_list
