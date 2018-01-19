from collections import OrderedDict
import logging

class Graph:
    def __init__(self, capacity):
        self.nodes = []
        self.breakpoints = []
        self.capacity = capacity
        self.current_gas = 0
        self.start = None
        self.goal = None

        #dynamic values
        self.tolerance_km = 0
        self.tolerance_amount = 0
        self.tolerance_price = 0.0
        self.fuel_surplus = 0
        self.tolerance_quotient = 1e-31

    def gas_for_km(self, km):
        return km * 0.056

    def km_for_gas(self, gas):
        return gas / 0.056

    # find cheapest predecessor for all nodes
    def find_prevs(self):
        self.breakpoints.append(self.goal)
        for n in self.nodes:
            cheapest = n
            for i in self.nodes[0:self.nodes.index(n)]:
                if self.gas_for_km(i.distance_to(n, self, True)) < self.capacity and i < cheapest:
                    cheapest = i
            n.prev = cheapest
            if n.prev == n:
                self.breakpoints.append(n)

    # find cheapest successor for all nodes
    def find_nexts(self):
        self.start.startpoint = True
        for n in self.nodes[0:len(self.nodes) - 1]:
            cheapest = self.nodes[self.nodes.index(n) + 1]
            for i in self.nodes[self.nodes.index(n) + 2:]:
                if n.startpoint is True and cheapest < n:
                    cheapest.startpoint = True
                    break
                if self.gas_for_km(n.distance_to(i, self, True)) < self.capacity and i < cheapest:
                    cheapest = i
            n.next = cheapest
            self.breakpoints.append(cheapest)

    #drive_route
    #@property
    def generate_refuel_infos(self):
        x = self.start
        self.breakpoints.sort(key=lambda bps: bps.datetime)
        bp = self.breakpoints
        gas_info = OrderedDict()
        tmp_refuels = OrderedDict()
        while x != self.goal:
            amount = 0
            x.current_gas = self.current_gas
            if bp and (x.price > x.next.price or x.price > x.prev.price):
                if self.current_gas >= self.gas_for_km(x.distance_to(x.next, self, True)):
                    self.current_gas -= self.gas_for_km(x.distance_to(x.next, self, None))
                else:
                    amount = self.gas_for_km(x.distance_to(x.next, self, True)) - self.current_gas
                    tmp_refuels[x.key] = amount
                    gas_info[x.id] = [amount, x.price_for_gas(amount)]
                    self.current_gas += gas_info[x.id][0] - self.gas_for_km(x.distance_to(x.next, self, None))
                next_x = x.next
                x.expected_amount = amount
                bp.remove(x)
                x = next_x
            else:
                amount = min(self.capacity, x.distance_to(self.goal, self, True)) - self.current_gas
                gas_info[x.id] = [amount, x.price_for_gas(amount)]
                tmp_refuels[x.key] = amount
                self.current_gas = self.current_gas + amount - self.gas_for_km(x.distance_to(x.next, self, None))
                next_x=x.next
                x.expected_amount = amount
                bp.remove(x)
                x = next_x
        optimizer_dict = []
        for n in self.nodes:
            if n.expected_amount > 0:
                optimizer_dict.append(n)
        while True:
            old_len = len(optimizer_dict)
            for i in range(1, len(optimizer_dict) - 1):
                try:
                    if (optimizer_dict[i].expected_amount < self.tolerance_amount and
                            optimizer_dict[i].price > max(optimizer_dict[i-1].price,
                                                          optimizer_dict[i+1].price) - self.tolerance_price and
                            self.gas_for_km(optimizer_dict[i-1].distance_to(optimizer_dict[i+1], self, True)) <
                            self.capacity):
                        optimizer_dict[i-1].expected_amount += optimizer_dict[i].expected_amount
                        optimizer_dict[i].current_gas += optimizer_dict[i].expected_amount
                        optimizer_dict[i].expected_amount = 0
                        optimizer_dict.pop(i)
                except IndexError:
                    pass
            if len(optimizer_dict) == old_len:
                break
        if len(optimizer_dict) > 1:
            while True:
                if optimizer_dict[-1].price > optimizer_dict[-2].price - self.tolerance_price / self.tolerance_quotient:
                    optimizer_dict.pop(-1)
                    optimizer_dict[-1].expected_amount = self.capacity
                    if len(optimizer_dict) == 1:
                        break
                else:
                    break
        optimizer_dict[-1].expected_amount = min(self.capacity, self.fuel_surplus +
                                                 self.gas_for_km(optimizer_dict[-1].distance_to(self.goal, self, True)))
        for node in self.nodes:
            node.expected_amount = min(abs(node.expected_amount), self.gas_for_km(node.distance_to(self.goal, self, True)))
        return [(x.datetime, x.id, x.price, x.expected_amount) for x in self.nodes]
