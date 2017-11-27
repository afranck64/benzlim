import collections

class Graph:
    start = None
    goal = None
    nodes = []
    breakpoints = []
    capacity = 0
    max_km = 0
    gasInfo = {}
    
    def __init__(self, capacity):
        self.capacity = capacity
        self.current_gas = self.capacity

    def gas_for_km(self, km):
        return km * 0.056

    def km_for_gas(self, gas):
        return gas / 0.056

    #find cheapest predecessor for all nodes
    def find_prevs(self):
        for n in self.nodes:
            cheapest = n
            for i in self.nodes[0:self.nodes.index(n)]:
                if i.distance_to(n) < self.capacity and i < cheapest:
                    cheapest = i
            n.prev = cheapest
            if n.prev == n:
                self.breakpoints.append(n)

    # find cheapest successor for all nodes
    def find_nexts(self):
        for n in self.nodes[0:len(self.nodes)-1]:
            cheapest = self.nodes[self.nodes.index(n)+1]
            for i in self.nodes[self.nodes.index(n)+2:len(self.nodes)]:
                #print("new cheapest?")
                if n.distance_to(i) < self.capacity and i < cheapest:
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
        for element in self.breakpoints:
            print(element.id)
        bp = self.breakpoints
        gas_info = {}

        while x != self.goal:
            print(self.current_gas)
            print(x.id)
            if bp and x != bp[0] and self.gas_for_km(x.distance_to(bp[0])) < self.capacity:
                if self.current_gas >= self.gas_for_km(x.distance_to(bp[0])): #If there is enough gas left in tank, don't fill up
                    self.current_gas -= self.gas_for_km(x.distance_to(bp[0]))
                else:
                    gas_info[x.id] = self.gas_for_km(x.distance_to(bp[0])) - self.current_gas
                    self.current_gas += gas_info[x.id] - self.gas_for_km(x.distance_to(bp[0]))
                x = bp.pop(0)
            else:
                if self.capacity - self.current_gas > 0:
                    gas_info[x.id] = self.capacity - self.current_gas
                self.current_gas -= self.gas_for_km(x.distance_to(x.next))
                x = x.next
        od = collections.OrderedDict(sorted(gas_info.items()))
        return od
