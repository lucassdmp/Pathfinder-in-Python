from random import randint
from time import perf_counter
import src.Node as nd
from openpyxl import Workbook
from src.Styles import headerStyle, cellAlignment
from src.FindPathFunction import aStarDBNH, aStarHaversine, breadthFirstSearch, depthFirstSearch, bestFirstSearch
from src.CalculatePathFunctions import pathInLatLon
from datetime import datetime


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

    collumns = ["A", "B", "C", "D", "E"]
    collumnsTitle = ["Algorithm", "Time", "Expanded Nodes", "Memory", "Path"]
    functions = [aStarDBNH, aStarHaversine, breadthFirstSearch, depthFirstSearch, bestFirstSearch]

    startTime = perf_counter()
    count = 1
    for sheet in wb:
        for i in range(len(collumns)):
            sheet[collumns[i] + "1"] = collumnsTitle[i]
            sheet[collumns[i] + "1"].style = headerStyle
            sheet.column_dimensions[collumns[i]].width = 30
            
        firstValue = randint(1, NODES)
        secondValue = randint(1, NODES)
        print("Teste " + str(count) + " de " + str(amountOfTests))

        for function in functions:
            Content = function(nodes, firstValue, secondValue, timeLimitSeconds)
            timeLimit = ""
            pathInLL = ""
            if Content[3] < timeLimitSeconds:
                timeLimit = Content[3]
            else:
                timeLimit = "Time Limit Exceeded"

            if Content[0]:
                pathInLL = pathInLatLon(nodes, Content[0])
            else:
                pathInLL = "No Path Found"
            
            sheet.append([Content[4], timeLimit, Content[2], Content[1], pathInLL])
        count += 1
        for i in range(2, 7):
            sheet['E'+str(i)].alignment = cellAlignment
            
        sheet["A9"] = "First Node"
        sheet["B9"] = "Second Node"
        sheet["A10"] = firstValue
        sheet["B10"] = secondValue
        sheet['A9'].style = headerStyle
        sheet['B9'].style = headerStyle

    CurrentTimeToStr = datetime.now().strftime("%d-%m-%Y %H-%M-%S")
    wookBookFilename = "Relátorio - " + filename + " - "+CurrentTimeToStr+".xlsx"

    wb[0]['B13'] = "Tempo de execução: " + str(perf_counter() - startTime) + " segundos"
    
    wb.save(wookBookFilename)


if __name__ == "__main__":
    main()
