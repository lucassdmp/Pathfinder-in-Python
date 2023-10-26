from cmath import sqrt
import operator
import random
import src.Node as nd
from time import sleep, perf_counter
from psutil import Process
from openpyxl import Workbook
import math
from src.Styles import headerStyle, cellAlignment

def haversineDistance(node1, node2):
    lat1 = math.radians(node1.lat) / 1000000
    lon1 = math.radians(node1.lon) / 1000000
    lat2 = math.radians(node2.lat) / 1000000
    lon2 = math.radians(node2.lon) / 1000000

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = (
        math.sin(dlat / 2) ** 2
        + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    )
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    R = 6371
    distance = R * c

    return distance


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


def loadLatLonFromNodes(graph: list, filename):
    coordfile = open(filename, "r")
    for line in coordfile:
        splitedLine = line.split()
        if splitedLine[0] == "v":
            graph[int(splitedLine[1])].lat = int(splitedLine[3])
            graph[int(splitedLine[1])].lon = int(splitedLine[2])
        else:
            continue

    coordfile.close()


def pathInLatLon(graph: list, path: list):
    pathLatLon = ""
    for node in path:
        pathLatLon += (
            "("
            + str(graph[node].lat / 1000000)
            + " "
            + str(graph[node].lon / 1000000)
            + ")"
        )
    return pathLatLon


def breadthFirstSearch(graph: list, start: int, end: int, timeLimitSeconds):
    startTime = perf_counter()
    startMemory = Process().memory_info().rss

    queuedNodes = [start]
    visitedNodes = set()
    nodeParent = {}
    path = []
    expandedNodes = 0

    while queuedNodes is not []:
        if perf_counter() - startTime > timeLimitSeconds:
            return (
                [],
                expandedNodes,
                Process().memory_info().rss - startMemory,
                perf_counter() - startTime,
            )

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
        return (
            [],
            expandedNodes,
            Process().memory_info().rss - startMemory,
            perf_counter() - startTime,
        )

    return (
        calculatePath(start, end, nodeParent),
        expandedNodes,
        Process().memory_info().rss - startMemory,
        perf_counter() - startTime,
    )


def depthFirstSearch(graph: list, start: int, end: int, timeLimitSeconds=120):
    startTime = perf_counter()
    startMemory = Process().memory_info().rss

    path = []
    visitedNodes = set()
    nodeParent = {}
    stackedNodes = [start]
    expandedNodes = 0

    while stackedNodes:
        if perf_counter() - startTime > timeLimitSeconds:
            return (
                [],
                expandedNodes,
                Process().memory_info().rss - startMemory,
                perf_counter() - startTime,
            )
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

    return (
        calculatePath(start, end, nodeParent),
        expandedNodes,
        Process().memory_info().rss - startMemory,
        perf_counter() - startTime,
    )


def bestFirstSearch(graph: list, start: int, end: int, timeLimitSeconds=120):
    startTime = perf_counter()
    startMemory = Process().memory_info().rss

    queuedNodes = [(graph[start], 0)]
    visitedNodes = set()
    nodeParent = {}
    expandedNodes = 0

    while queuedNodes is not []:
        if perf_counter() - startTime > timeLimitSeconds:
            return (
                [],
                expandedNodes,
                Process().memory_info().rss - startMemory,
                perf_counter() - startTime,
            )

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
        return (
            [],
            expandedNodes,
            Process().memory_info().rss - startMemory,
            perf_counter() - startTime,
        )

    return (
        calculatePath(start, end, nodeParent),
        expandedNodes,
        Process().memory_info().rss - startMemory,
        perf_counter() - startTime,
    )


def aStarDBNH(graph: list, start: int, end: int, timeLimitSeconds=120):
    startTime = perf_counter()
    startMemory = Process().memory_info().rss

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
            if (
                connectedNodeTuple[0] not in visitedNodes
                and connectedNode not in queuedNodes
            ):
                queuedNodes.append(connectedNode)
                nodeParent[connectedNode.value] = currentNode.value
                connectedNode.distHeuristic = calculateDistanceBetweenNodes(
                    endNode, connectedNode
                )

        queuedNodes.sort(key=operator.attrgetter("distHeuristic"))

    if end not in nodeParent:
        return (
            [],
            expandedNodes,
            Process().memory_info().rss - startMemory,
            perf_counter() - startTime,
        )

    return (
        calculatePath(start, end, nodeParent),
        expandedNodes,
        Process().memory_info().rss - startMemory,
        perf_counter() - startTime,
    )


def aStarHaversine(graph: list, start: int, end: int, timeLimitSeconds=120):
    startTime = perf_counter()
    startMemory = Process().memory_info().rss

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
            if (
                connectedNodeTuple[0] not in visitedNodes
                and connectedNode not in queuedNodes
            ):
                queuedNodes.append(connectedNode)
                nodeParent[connectedNode.value] = currentNode.value
                connectedNode.distHeuristic = haversineDistance(endNode, connectedNode)

        queuedNodes.sort(key=operator.attrgetter("distHeuristic"))

    if end not in nodeParent:
        return (
            [],
            expandedNodes,
            Process().memory_info().rss - startMemory,
            perf_counter() - startTime,
        )

    return (
        calculatePath(start, end, nodeParent),
        expandedNodes,
        Process().memory_info().rss - startMemory,
        perf_counter() - startTime,
    )


def main():
    file = open("files.txt", "r")
    fileOptions = []
    for line in file:
        fileOptions.append(line.strip())

    file.close()
    print("Escolha um arquivo:")
    for i in range(len(fileOptions)):
        print(str(i + 1) + " - " + fileOptions[i])

    filename = fileOptions[int(input()) - 1]
    graphFile = filename + ".gr"
    coordFile = filename + ".co"

    print("Escolha o tempo limite em segundos: ")
    timeLimitSeconds = abs(int(input()))

    print("Escolha a quantidade de testes: ")
    amountOfTests = abs(int(input()))

    file = open(graphFile, "r")

    for line in file:
        if line[0] == "p":
            _, _, NODES, _ = line.split()
            break
        elif line[0] == "v":
            file.seek(0)
            break
        else:
            continue

    NODES = int(NODES)

    nodes = []
    for i in range(NODES + 1):
        nodes.append(nd.Node(i))

    for line in file:
        if line[0] == "a":
            _, node1, node2, weight = line.split()
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

    loadLatLonFromNodes(nodes, coordFile)
    
    print('starting tests...')
    #A* DBNH and A* Haversine
    firstValue = 441116
    secondValue = 2163016
    print("first node: ", firstValue)
    print("second node: ", secondValue)
    Content = aStarDBNH(nodes, firstValue, secondValue, timeLimitSeconds)
    print("A* DBNH")
    print("Expanded Nodes: " + str(Content[1]))
    print("Memory: " + str(Content[2]))
    print("Time: " + str(Content[3]))
    print("first node: ", firstValue)
    print("second node: ", secondValue)
    
    Content = aStarHaversine(nodes, firstValue, secondValue, timeLimitSeconds)
    print("A* Haversine")
    print("Expanded Nodes: " + str(Content[1]))
    print("Memory: " + str(Content[2]))
    print("Time: " + str(Content[3]))

    # wb = Workbook()
    # wb.add_named_style(headerStyle)
    # for i in range(2, amountOfTests + 1):
    #     wb.create_sheet("Relátorio " + str(i))

    # wb.active.title = "Relátorio 1"

    # collumns = ["A", "B", "C", "D", "E", "G", "H"]
    # collumnsTitle = ["Algorithm", "Time", "Expanded Nodes", "Memory", "Path", "First Node", "Second Node"]

    # for sheet in wb:
    #     firstValue = random.randint(1, NODES)
    #     secondValue = random.randint(1, NODES)
        
    #     sheet["G2"] = firstValue
    #     sheet["H2"] = secondValue
        
    #     Content = breadthFirstSearch(nodes, firstValue, secondValue, timeLimitSeconds)
    #     sheet["A2"] = "Breadth First Search"
    #     sheet["C2"] = Content[2]
    #     sheet["D2"] = Content[1]

    #     if Content[3] < timeLimitSeconds:
    #         sheet["B2"] = Content[3]
    #     else:
    #         sheet["B2"] = "Time Limit Exceeded"

    #     if Content[0]:
    #         sheet["E2"] = pathInLatLon(nodes, Content[0])
    #     else:
    #         sheet["E2"] = "No Path Found"

    #     Content = depthFirstSearch(nodes, firstValue, secondValue, timeLimitSeconds)
    #     sheet["A3"] = "Depth First Search"
    #     sheet["C3"] = Content[2]
    #     sheet["D3"] = Content[1]

    #     if Content[3] < timeLimitSeconds:
    #         sheet["B3"] = Content[3]
    #     else:
    #         sheet["B3"] = "Time Limit Exceeded"

    #     if Content[0]:
    #         sheet["E3"] = pathInLatLon(nodes, Content[0])
    #     else:
    #         sheet["E3"] = "No Path Found"

    #     Content = bestFirstSearch(nodes, firstValue, secondValue, timeLimitSeconds)
    #     sheet["A4"] = "Best First Search"
    #     sheet["C4"] = Content[2]
    #     sheet["D4"] = Content[1]

    #     if Content[3] < timeLimitSeconds:
    #         sheet["B4"] = Content[3]
    #     else:
    #         sheet["B4"] = "Time Limit Exceeded"

    #     if Content[0]:
    #         sheet["E4"] = pathInLatLon(nodes, Content[0])
    #     else:
    #         sheet["E4"] = "No Path Found"

    #     Content = aStarDBNH(nodes, firstValue, secondValue, timeLimitSeconds)
    #     sheet["A5"] = "A* DBNH"
    #     sheet["C5"] = Content[2]
    #     sheet["D5"] = Content[1]

    #     if Content[3] < timeLimitSeconds:
    #         sheet["B5"] = Content[3]
    #     else:
    #         sheet["B5"] = "Time Limit Exceeded"

    #     if Content[0]:
    #         sheet["E5"] = pathInLatLon(nodes, Content[0])
    #     else:
    #         sheet["E5"] = "No Path Found"

    #     Content = aStarHaversine(nodes, firstValue, secondValue, timeLimitSeconds)
    #     sheet["A6"] = "A* Haversine"
    #     sheet["C6"] = Content[2]
    #     sheet["D6"] = Content[1]

    #     if Content[3] < timeLimitSeconds:
    #         sheet["B6"] = Content[3]
    #     else:
    #         sheet["B6"] = "Time Limit Exceeded"

    #     if Content[0]:
    #         sheet["E6"] = pathInLatLon(nodes, Content[0])
    #     else:
    #         sheet["E6"] = "No Path Found"
            
    #     for i in range(len(collumns)):
    #         sheet[collumns[i] + "1"] = collumnsTitle[i]
    #         sheet[collumns[i] + "1"].style = headerStyle
    #         sheet.column_dimensions[collumns[i]].width = 30
            
    #     for i in range(2, 7):
    #         sheet['E'+str(i)].alignment = cellAlignment

    # wb.save("Relátorio.xlsx")


if __name__ == "__main__":
    main()
