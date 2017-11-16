class Graph:
    EPS = 1
    start = None
    goal = None
    nodes = []
    breakpoints = []
    capacity = 0
    max_km = 0
    gasInfo = {}
    
    def __init__(self, capacity):
        self.capacity = capacity
        self.current_gas = capacity

    def gas_for_km(self, km):
        return km / 10
        #todo: Should be car-specific

    def km_for_gas(self, gas):
        return gas * 10

    def find_prevs(self):
        for n in self.nodes:
            cheapest = n
            for i in self.nodes[0:self.nodes.index(n)]:
                if i.distance_to(n) < self.capacity and i < cheapest:
                    cheapest = i
            n.prev = cheapest
            if n.prev == n:
                self.breakpoints.append(n)
                 
    def find_nexts(self):
        for n in self.nodes[0:len(self.nodes)-1]:
            cheapest = self.nodes[self.nodes.index(n)+1]
            for i in self.nodes[self.nodes.index(n)+2:len(self.nodes)]:
                if n.distance_to(i) < self.capacity and i < cheapest:
                    cheapest = i
            n.next = cheapest
            
    def drive_to_next(self):
        x = self.start
        bp = self.breakpoints
        gas_info = {}

        while x.distance_to(self.goal) > self.EPS:
            if bp and x.distance_to(bp[0]) > 0 and self.gas_for_km(x.distance_to(bp[0])) < self.capacity:
                gas_info[x.id] = self.current_gas - self.gas_for_km(x.distance_to(bp[0]))
                self.current_gas += self.gas_for_km(x.distance_to(bp[0])) - self.gas_for_km(x.distance_to(bp[0]))
                x = self.breakpoints.pop(0)
            else:
                self.current_gas -= self.gas_for_km(x.distance_to(x.next))
                gas_info[x.id] = self.capacity - self.current_gas
                self.current_gas = self.capacity
                x = x.next
        print(gas_info)


'''
DRIVE-TO-NEXT(i, k)
1 Let x be i.
2 If d xk ≤ U then just fill enough gas to go k.
3 Otherwise, fill up and drive to next(x). Let x be next(x), go to step 2.
'''
