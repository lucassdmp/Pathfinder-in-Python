import heapq

class PriorityQueueElement:
    def __init__(self, tuple_element):
        self.tuple_element = tuple_element

    def __lt__(self, other):
        return self.tuple_element[1] < other.tuple_element[1]

class PriorityQueue:
    def __init__(self):
        self.queue = []
        
    def push(self, element):
        heapq.heappush(self.queue, PriorityQueueElement(element))
        
    def pop(self):
        return heapq.heappop(self.queue).tuple_element