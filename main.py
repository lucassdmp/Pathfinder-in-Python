import operator
import Node as nd
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
    
    return path

def bestFirstSearch(graph: list, start: int, end: int):
    queuedNodes = [(start, 0)]
    visitedNodes = set()
    nodeParent = {}
    
    while queuedNodes is not []:
        # for node in queuedNodes:
        #     print(node[0].value, node[1], end=" ")
        # print()
        currentNodeTuple = queuedNodes.pop(0)
        currentNode = graph[currentNodeTuple[0]]
        currentNodeCost = currentNodeTuple[1]
        
        if currentNode.value == end:
            break
        
        for connectedNode in currentNode.connectedNodes:
            if connectedNode[0] not in visitedNodes:
                nodeParent[connectedNode[0]] = currentNode.value
                costToConnectedNode = currentNodeCost + connectedNode[1]
                queuedNodes.append((connectedNode[0], costToConnectedNode))
                
        queuedNodes.sort(key=operator.itemgetter(1))
        # for node in queuedNodes:
        #     print(graph[node[0]].value, node[1], end=",")
        # print()
        
        
    if end not in nodeParent:
        return None
    
    return calculatePath(start, end, nodeParent)

def main():
    # read file NewYork.gr
    file = open("NewYork.gr", "r")
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
    startTimeBFS = time.perf_counter()
    print(breadthFirstSearch(nodes, 1, 3))
    endTimeBFS = time.perf_counter()
    print("BrFS time: ", endTimeBFS - startTimeBFS, "seconds")

    # startTimeDFS = time.perf_counter()
    # depthFirstSearch(nodes, 1, 6000)
    # endTimeDFS = time.perf_counter()
    # print("DFS time: ", endTimeDFS - startTimeDFS, "seconds")

    startTimeBFS = time.perf_counter()
    print(bestFirstSearch(nodes, 1, 3))
    endTimeBFS = time.perf_counter()
    print("BFS time: ", endTimeBFS - startTimeBFS, "seconds")

if __name__ == "__main__":
    main()
