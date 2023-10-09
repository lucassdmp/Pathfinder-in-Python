from cmath import sqrt
import operator
import random
import src.Node as nd
import time

def breadthFirstSearch(graph: list, start: int, end: int):
    queuedNodes = [start]
    visitedNodes = set()
    nodeParent = {}
    path = []

    while queuedNodes is not []:
        currentNode = queuedNodes.pop(0)
        visitedNodes.add(currentNode)

        if currentNode == end:
            break

        for connectedNode in graph[currentNode].connectedNodes:
            if connectedNode[0] not in visitedNodes:
                queuedNodes.append(connectedNode[0])
                nodeParent[connectedNode[0]] = currentNode

    if end not in nodeParent:
        return None

    return calculatePath(start, end, nodeParent)

def depthFirstSearch(graph: list, start: int, end: int):
    path = []
    visitedNodes = set()
    nodeParent = {}
    stackedNodes = [start]

    while stackedNodes:
        currentNode = stackedNodes.pop()

        if currentNode == end:
            break

        for connectedNode in graph[currentNode].connectedNodes:
            if connectedNode[0] not in visitedNodes:
                stackedNodes.append(connectedNode[0])
                visitedNodes.add(currentNode)
                nodeParent[connectedNode[0]] = currentNode

    if end not in nodeParent:
        return None

    return calculatePath(start, end, nodeParent)

def calculatePath(start, finish, parentSet):
    currentNode = finish
    path = []

    while currentNode != start:
        path.append(currentNode)
        currentNode = parentSet[currentNode]
    path.append(start)
    
    return path[::-1]

def bestFirstSearch(graph: list, start: int, end: int):
    queuedNodes = [(graph[start], 0)]
    visitedNodes = set()
    nodeParent = {}
    
    while queuedNodes is not []:
        nodeTupple = queuedNodes.pop(0)
        node = nodeTupple[0]
        nodeCost = nodeTupple[1]
        visitedNodes.add(node.value)
        
        if node.value == end:
            break
        
        for connectedNodeTuple in node.connectedNodes:
            connectedNode = graph[connectedNodeTuple[0]]
            connectedNodeCost = connectedNodeTuple[1]
            if connectedNodeTuple[0] not in visitedNodes and connectedNode not in queuedNodes:
                queuedNodes.append((connectedNode, connectedNodeCost))
                nodeParent[connectedNode.value] = node.value
        queuedNodes.sort(key=operator.itemgetter(1))
        
    if end not in nodeParent:
        return None
    
    return calculatePath(start, end, nodeParent)

def calculateDistanceBetweenNodes(node1, node2):
    return int(sqrt(((node1.lat - node2.lat) * (node1.lat - node2.lat)) + ((node1.lon - node2.lon) * (node1.lon - node2.lon))).real)

def aStarDBNH(graph: list, start: int, end: int, coordFile):
    visitedNodes = set()
    queuedNodes = [graph[start]]
    endNode = graph[end]
    nodeParent = {}
       
    while queuedNodes is not []:
        currentNode = queuedNodes.pop(0)
        visitedNodes.add(currentNode.value)
        
        if(currentNode.value == end):
            break
            
        for connectedNodeTuple in currentNode.connectedNodes:
            connectedNode = graph[connectedNodeTuple[0]]
            connectionDistance = connectedNodeTuple[1]
            if connectedNodeTuple[0] not in visitedNodes and connectedNode not in queuedNodes:
                queuedNodes.append(connectedNode)
                nodeParent[connectedNode.value] = currentNode.value
                connectedNode.heuristic = calculateDistanceBetweenNodes(endNode, connectedNode)
                connectedNode.distToRoot = currentNode.distToRoot + connectionDistance
                connectedNode.distTotal = connectedNode.distToRoot + connectedNode.distHeuristic

        queuedNodes.sort(key=operator.attrgetter("distTotal"))
        
    if end not in nodeParent:
        return None

    return calculatePath(start, end, nodeParent)
         

def loadLatLonFromNodes(graph: list, filename):
    coordfile = open(filename, "r")

    for line in coordfile:
        splitedLine = line.split()
        if splitedLine[0] == 'v':
            graph[int(splitedLine[1])].lat = int(splitedLine[3])
            graph[int(splitedLine[1])].lon = int(splitedLine[2])
           
def main():
    # read file NewYork.gr
    filename = 'USA_West'
    graphFile = filename + '.gr'
    coordFile = filename + '.co'
    
    file = open(graphFile, "r")
    actionP, NODES, Conn = file.readline().split()
    NODES = int(NODES)

    # create nodes
    nodes = []
    for i in range(NODES + 1):
        nodes.append(nd.Node(i))

    for line in file:
        a, node1, node2, weight = line.split()
        if a == "a":
            node1 = int(node1)
            node2 = int(node2)
            weight = int(weight)
            if not nodes[node1].doesConnectionExist((node2, weight)):
                nodes[node1].addConnection((node2, weight))
            if not nodes[node2].doesConnectionExist((node1, weight)):
                nodes[node2].addConnection((node1, weight))
        else:
            continue

    # file.close()
    # startTimeBFS = time.perf_counter()
    # print(breadthFirstSearch(nodes, 120000, 243552))
    # endTimeBFS = time.perf_counter()
    # print("BrFS time: ", endTimeBFS - startTimeBFS, "seconds")

    # startTimeDFS = time.perf_counter()
    # depthFirstSearch(nodes, 1, 6000)
    # endTimeDFS = time.perf_counter()
    # print("DFS time: ", endTimeDFS - startTimeDFS, "seconds")

    firstValue = random.randint(1, NODES)
    secondValue = random.randint(1, NODES)
    
    print("Putting Coords in Nodes")
    loadLatLonFromNodes(nodes, secondValue, coordFile)
    print("Finished Putting Coords in Nodes")

    startTimeBFS = time.perf_counter()
    print(aStarDBNH(nodes, firstValue, secondValue, coordFile))
    endTimeBFS = time.perf_counter()
    print("A* time: ", endTimeBFS - startTimeBFS, "seconds")
    
    # startTimeBFS = time.perf_counter()
    # print(bestFirstSearch(nodes, firstValue, secondValue))
    # endTimeBFS = time.perf_counter()
    # print("BFS time: ", endTimeBFS - startTimeBFS, "seconds")
    
if __name__ == "__main__":
    main()
