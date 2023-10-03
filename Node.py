class Node:
    def __init__(self, value):
        self.value = value
        self.connectedNodes = []
        
    def addConnection(self, connection):
        if connection not in self.connectedNodes:
            self.connectedNodes.append(connection)
            
    def doesConnectionExist(self, connection):
        if connection in self.connectedNodes:
            return True
        else:
            return False