from random import randint
import src.Node as nd
from openpyxl import Workbook
from src.Styles import headerStyle, cellAlignment
from src.FindPathFunction import aStarDBNH, aStarHaversine, breadthFirstSearch, depthFirstSearch, bestFirstSearch
from src.CalculatePathFunctions import pathInLatLon

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

    wb = Workbook()
    wb.add_named_style(headerStyle)
    for i in range(2, amountOfTests + 1):
        wb.create_sheet("Relátorio " + str(i))

    wb.active.title = "Relátorio 1"

    collumns = ["A", "B", "C", "D", "E", "G", "H"]
    collumnsTitle = ["Algorithm", "Time", "Expanded Nodes", "Memory", "Path"]

    for sheet in wb:
        firstValue = randint(1, NODES)
        secondValue = randint(1, NODES)

        sheet["A9"] = "First Node"
        sheet["B9"] = "Second Node"
        sheet["A10"] = firstValue
        sheet["B10"] = secondValue
        sheet['A9'].style = headerStyle
        sheet['B9'].style = headerStyle

        Content = breadthFirstSearch(nodes, firstValue, secondValue, timeLimitSeconds)
        sheet["A2"] = "Breadth First Search"
        sheet["C2"] = Content[2]
        sheet["D2"] = Content[1]

        if Content[3] < timeLimitSeconds:
            sheet["B2"] = Content[3]
        else:
            sheet["B2"] = "Time Limit Exceeded"

        if Content[0]:
            sheet["E2"] = pathInLatLon(nodes, Content[0])
        else:
            sheet["E2"] = "No Path Found"

        Content = depthFirstSearch(nodes, firstValue, secondValue, timeLimitSeconds)
        sheet["A3"] = "Depth First Search"
        sheet["C3"] = Content[2]
        sheet["D3"] = Content[1]

        if Content[3] < timeLimitSeconds:
            sheet["B3"] = Content[3]
        else:
            sheet["B3"] = "Time Limit Exceeded"

        if Content[0]:
            sheet["E3"] = pathInLatLon(nodes, Content[0])
        else:
            sheet["E3"] = "No Path Found"

        Content = bestFirstSearch(nodes, firstValue, secondValue, timeLimitSeconds)
        sheet["A4"] = "Best First Search"
        sheet["C4"] = Content[2]
        sheet["D4"] = Content[1]

        if Content[3] < timeLimitSeconds:
            sheet["B4"] = Content[3]
        else:
            sheet["B4"] = "Time Limit Exceeded"

        if Content[0]:
            sheet["E4"] = pathInLatLon(nodes, Content[0])
        else:
            sheet["E4"] = "No Path Found"

        Content = aStarDBNH(nodes, firstValue, secondValue, timeLimitSeconds)
        sheet["A5"] = "A* DBNH"
        sheet["C5"] = Content[2]
        sheet["D5"] = Content[1]

        if Content[3] < timeLimitSeconds:
            sheet["B5"] = Content[3]
        else:
            sheet["B5"] = "Time Limit Exceeded"

        if Content[0]:
            sheet["E5"] = pathInLatLon(nodes, Content[0])
        else:
            sheet["E5"] = "No Path Found"

        Content = aStarHaversine(nodes, firstValue, secondValue, timeLimitSeconds)
        sheet["A6"] = "A* Haversine"
        sheet["C6"] = Content[2]
        sheet["D6"] = Content[1]

        if Content[3] < timeLimitSeconds:
            sheet["B6"] = Content[3]
        else:
            sheet["B6"] = "Time Limit Exceeded"

        if Content[0]:
            sheet["E6"] = pathInLatLon(nodes, Content[0])
        else:
            sheet["E6"] = "No Path Found"

        for i in range(len(collumns)):
            sheet[collumns[i] + "1"] = collumnsTitle[i]
            sheet[collumns[i] + "1"].style = headerStyle
            sheet.column_dimensions[collumns[i]].width = 30

        for i in range(2, 7):
            sheet['E'+str(i)].alignment = cellAlignment

    wb.save("Relátorio.xlsx")


if __name__ == "__main__":
    main()
