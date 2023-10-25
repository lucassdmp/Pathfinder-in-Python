from cmath import sqrt
import operator
import random
import src.Node as nd
import time
import psutil


def breadthFirstSearch(graph: list, start: int, end: int):
    startTime = time.perf_counter()
    queuedNodes = [start]
    visitedNodes = set()
    nodeParent = {}
    path = []
    expandedNodes = 0

    while queuedNodes is not []:
        if time.perf_counter() - startTime > 120:
            return ([], expandedNodes)

        currentNode = queuedNodes.pop(0)
        expandedNodes += 1
        visitedNodes.add(currentNode)

        if currentNode == end:
            break

        for connectedNode in graph[currentNode].connectedNodes:
            if connectedNode[0] not in visitedNodes:
                queuedNodes.append(connectedNode[0])
                nodeParent[connectedNode[0]] = currentNode

    if end not in nodeParent:
        return ([], expandedNodes)

    return (calculatePath(start, end, nodeParent), expandedNodes)


def depthFirstSearch(graph: list, start: int, end: int):
    startTime = time.perf_counter()
    path = []
    visitedNodes = set()
    nodeParent = {}
    stackedNodes = [start]
    expandedNodes = 0

    while stackedNodes:
        if time.perf_counter() - startTime > 120:
            return ([], expandedNodes)
        currentNode = stackedNodes.pop()
        expandedNodes += 1

        if currentNode == end:
            break

        for connectedNode in graph[currentNode].connectedNodes:
            if connectedNode[0] not in visitedNodes:
                stackedNodes.append(connectedNode[0])
                visitedNodes.add(currentNode)
                nodeParent[connectedNode[0]] = currentNode

    if end not in nodeParent:
        return ([], expandedNodes)

    return (calculatePath(start, end, nodeParent), expandedNodes)


def bestFirstSearch(graph: list, start: int, end: int):
    startTime = time.perf_counter()
    queuedNodes = [(graph[start], 0)]
    visitedNodes = set()
    nodeParent = {}
    expandedNodes = 0

    while queuedNodes is not []:
        if time.perf_counter() - startTime > 120:
            return ([], expandedNodes)

        nodeTupple = queuedNodes.pop(0)
        node = nodeTupple[0]
        nodeCost = nodeTupple[1]
        visitedNodes.add(node.value)
        expandedNodes += 1

        if node.value == end:
            break

        for connectedNodeTuple in node.connectedNodes:
            connectedNode = graph[connectedNodeTuple[0]]
            connectedNodeCost = connectedNodeTuple[1]
            if (
                connectedNodeTuple[0] not in visitedNodes
                and connectedNode not in queuedNodes
            ):
                queuedNodes.append((connectedNode, connectedNodeCost))
                nodeParent[connectedNode.value] = node.value
        queuedNodes.sort(key=operator.itemgetter(1))

    if end not in nodeParent:
        return ([], expandedNodes)

    return (calculatePath(start, end, nodeParent), expandedNodes)


def calculatePath(start, finish, parentSet):
    currentNode = finish
    path = []

    while currentNode != start:
        path.append(currentNode)
        currentNode = parentSet[currentNode]
    path.append(start)

    return path[::-1]


def calculateDistanceBetweenNodes(node1, node2):
    return abs(
        int(
            sqrt(
                ((node1.lat - node2.lat) * (node1.lat - node2.lat))
                + ((node1.lon - node2.lon) * (node1.lon - node2.lon))
            ).real
        )
    )


def aStarDBNH(graph: list, start: int, end: int):
    visitedNodes = set()
    queuedNodes = [graph[start]]
    endNode = graph[end]
    nodeParent = {}
    expandedNodes = 0

    while queuedNodes is not []:
        currentNode = queuedNodes.pop(0)
        visitedNodes.add(currentNode.value)
        expandedNodes += 1
        if currentNode.value == end:
            break

        for connectedNodeTuple in currentNode.connectedNodes:
            connectedNode = graph[connectedNodeTuple[0]]
            # connectionDistance = connectedNodeTuple[1]
            if (
                connectedNodeTuple[0] not in visitedNodes
                and connectedNode not in queuedNodes
            ):
                queuedNodes.append(connectedNode)
                nodeParent[connectedNode.value] = currentNode.value
                connectedNode.heuristic = calculateDistanceBetweenNodes(
                    endNode, connectedNode
                )
                # connectedNode.distToRoot = currentNode.distToRoot + connectionDistance
                # connectedNode.distTotal = connectedNode.distToRoot + connectedNode.distHeuristic

        queuedNodes.sort(key=operator.attrgetter("heuristic"))

    if end not in nodeParent:
        return ([], expandedNodes)

    # print("done")
    return (calculatePath(start, end, nodeParent),expandedNodes)


def loadLatLonFromNodes(graph: list, filename):
    coordfile = open(filename, "r")

    for line in coordfile:
        splitedLine = line.split()
        if splitedLine[0] == "v":
            graph[int(splitedLine[1])].lat = int(splitedLine[3])
            graph[int(splitedLine[1])].lon = int(splitedLine[2])


def main():
    # read file NewYork.gr
    filename = "USA_West"
    graphFile = filename + ".gr"
    coordFile = filename + ".co"

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

    file.close()

    print("Putting Coords in Nodes")
    loadLatLonFromNodes(nodes, coordFile)
    print("Finished Putting Coords in Nodes")

    firstValue = random.randint(1, NODES)
    secondValue = random.randint(1, NODES)
    print("First value: ", firstValue)
    print("Second value: ", secondValue)
    
    startMemory = psutil.Process().memory_info().rss
    startTime = time.perf_counter()
    Elementos = breadthFirstSearch(nodes, firstValue, secondValue)
    print("Nos expandidos:", Elementos[1])
    endTime = time.perf_counter()
    endMemory = psutil.Process().memory_info().rss
    print("Memory used: ", endMemory - startMemory, "bytes")
    print("BrFS time: ", endTime - startTime, "seconds")
    
    time.sleep(5)
    
    startMemory = psutil.Process().memory_info().rss
    startTime = time.perf_counter()
    Elementos = depthFirstSearch(nodes, firstValue, secondValue) 
    print("Nos expandidos:", Elementos[1])
    endTime = time.perf_counter()
    endMemory = psutil.Process().memory_info().rss
    print("Memory used: ", endMemory - startMemory, "bytes")
    print("DFS time: ", endTime - startTime, "seconds")

    time.sleep(5)

    startMemory = psutil.Process().memory_info().rss
    startTime = time.perf_counter()
    Elementos = bestFirstSearch(nodes, firstValue, secondValue)
    print("Nos expandidos:", Elementos[1])
    endTime = time.perf_counter()
    endMemory = psutil.Process().memory_info().rss
    print("Memory used: ", endMemory - startMemory, "bytes")
    print("BFS time: ", endTime - startTime, "seconds")
    
    time.sleep(5)

    startMemory = psutil.Process().memory_info().rss
    startTime = time.perf_counter()
    Elementos = aStarDBNH(nodes, firstValue, secondValue)
    print("Nos expandidos:", Elementos[1])
    endTime = time.perf_counter()
    endMemory = psutil.Process().memory_info().rss
    print("Memory used: ", endMemory - startMemory, "bytes")
    print("A* time: ", endTime - startTime, "seconds")

    time.sleep(5)


if __name__ == "__main__":
    main()
