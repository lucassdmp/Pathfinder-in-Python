class Node:
    def __init__(self, value):
        self.value = value
        self.connectedNodes = []
        self.distHeuristic = 0
        
    def addConnection(self, connection):
        if connection not in self.connectedNodes:
            self.connectedNodes.append(connection)
            
    def doesConnectionExist(self, connection):
        return connection in self.connectedNodes