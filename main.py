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

def aStar(graph: list, start: int, end: int, coordFile, heuricticFunc):
    visitedNodes = set()
    queuedNodes = [graph[start]]
    nodeParent = {}
    
    print("Building Heuristic")
    heuricticFunc(graph, start, coordFile)
    print("Finished Building Heuristic")
    
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
                connectedNode.distToRoot = currentNode.distToRoot + connectionDistance
                connectedNode.distTotal = connectedNode.distToRoot + connectedNode.distHeuristic

        queuedNodes.sort(key=operator.attrgetter("distTotal"))
        
    if end not in nodeParent:
        return None

    return calculatePath(start, end, nodeParent)

##WORKING
def heuristicDistanceBetweenNodes(graph: list, start: int, filename):
    heuristicFile = open(filename, "r")
    startingNode = graph[start]
    NodeLat = 0
    NodeLong = 0
    
    for line in heuristicFile:
        splitedLine = line.split()
        if splitedLine[0] == 'v' and int(splitedLine[1]) == startingNode.value:
            NodeLat = int(splitedLine[3])
            NodeLong = int(splitedLine[2])
            break
    
    heuristicFile.seek(0)
    ##calculate distance between all points 
    for line in heuristicFile:
        splitedLine = line.split()
        if splitedLine[0] == 'v':
            graph[int(splitedLine[1])].lat = int(splitedLine[3])
            graph[int(splitedLine[1])].lon = int(splitedLine[2])
            
            latsSubtracted = int(splitedLine[3]) - NodeLat
            longsSubtracted = int(splitedLine[2]) - NodeLong
            graph[int(splitedLine[1])].distHeuristic =  int(sqrt((latsSubtracted * latsSubtracted) + (longsSubtracted * longsSubtracted)).real)
            
def main():
    # read file NewYork.gr
    filename = 'NewYork'
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

    firstValue = 154542 #random.randint(154542, 243400)
    secondValue = 243400 #random.randint(1, 243552)

    startTimeBFS = time.perf_counter()
    print(aStar(nodes, firstValue, secondValue, coordFile, heuristicDistanceBetweenNodes))
    endTimeBFS = time.perf_counter()
    print("BFS time: ", endTimeBFS - startTimeBFS, "seconds")

if __name__ == "__main__":
    main()
