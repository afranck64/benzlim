from collections import OrderedDict

class Graph:
    def __init__(self, capacity):
        self.nodes = []
        self.breakpoints = []
        self.capacity = capacity
        self.current_gas = 0
        self.start = None
        self.goal = None
        self.max_km = 0
        self.pos_index = 0

    def gas_for_km(self, km):
        return km * 0.056

    def km_for_gas(self, gas):
        return gas / 0.056

    #find cheapest predecessor for all nodes
    def find_prevs(self):
        for n in self.nodes:
            cheapest = n
            for i in self.nodes[0:self.nodes.index(n)]:
                if self.gas_for_km(i.distance_to(n)) < self.capacity and i < cheapest:
                    cheapest = i
            n.prev = cheapest
            if n.prev == n:
                self.breakpoints.append(n)

    # find cheapest successor for all nodes
    def find_nexts(self):
        for n in self.nodes[0:len(self.nodes)-1]:
            cheapest = self.nodes[self.nodes.index(n)+1]
            for i in self.nodes[self.nodes.index(n)+2:]:
                if self.gas_for_km(n.distance_to(i)) < self.capacity and i < cheapest:
                    cheapest = i
            n.next = cheapest

    '''
    DRIVE-TO-NEXT(i, k)
    1 Let x be i.
    2 If d xk <= U then just fill enough gas to go k.
    3 Otherwise, fill up and drive to next(x). Let x be next(x), go to step 2.
    '''
    def drive_to_next(self):
        x = self.start
        self.breakpoints.sort(key=lambda bps: bps.datetime)
        bp = self.breakpoints
        gas_info = OrderedDict()
        
        tmp_refuels = OrderedDict()
        while x != self.goal:
            if bp and x != bp[0] and self.gas_for_km(x.distance_to(bp[0])) < self.current_gas:
                if self.current_gas >= self.gas_for_km(x.distance_to(bp[0])): #If there is enough gas left in tank, don't fill up
                    self.current_gas -= self.gas_for_km(x.distance_to(bp[0]))
                else:
                    amount = self.gas_for_km(x.distance_to(bp[0])) - self.current_gas
                    tmp_refuels[x.key] = amount
                    gas_info[x.id] = [amount, x.price_for_gas(amount)]
                    self.current_gas += gas_info[x.id][0] - self.gas_for_km(x.distance_to(bp[0]))
                x = bp.pop(0)
            else:
                amount = min(self.capacity, self.gas_for_km(x.distance_to(self.nodes[-1]))) - self.current_gas
                if amount > 0:
                    gas_info[x.id] = [amount, x.price_for_gas(amount)]
                    tmp_refuels[x.key] = amount
                self.current_gas -= self.gas_for_km(x.distance_to(x.next))
                x = x.next
        refuel_infos = [(x.datetime, x.id, x.price, tmp_refuels.get(x.key, 0)) for x in self.nodes]
        return refuel_infos