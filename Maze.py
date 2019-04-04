#	Nama	:	Haris Salman / Ahmad Naufal Hakim
#	NIM		:	13517052 / 13517055
#	Tanggal	:	29 Maret 2019
#	Tugas Kecil 3 Strategi Algoritma : Algoritma BFS dan A*

import queue as q
import operator
import numpy as np
import matplotlib.pyplot as gui
from pathlib import Path

def readMaze(maze,name) :
    data = Path("map/"+name)
    with open(data ,'r') as f :
        for line in f :
            line = line.rstrip()
            row = []
            for value in line :
                row.append((int)(value))
            maze.append(row)

def print_maze(maze):
    maze = np.array(maze)
    row,col = maze.shape
    for i in range(row):
        for j in range(col):
            if(maze[i][j]==1):
                print("██",end ="")
            elif (maze[i][j]==0):
                print("  ",end ="")
            elif (maze[i][j]==2):
                print(" .",end ="")
            elif(maze[i][j]==3):
                print(" ☺",end ="")
        print()

    gui.pcolormesh(maze)
    gui.axes().set_aspect('equal') #set the x and y axes to the same scale
    gui.xticks([]) # remove the tick marks by setting to an empty list
    gui.yticks([]) # remove the tick marks by setting to an empty list
    gui.axes().invert_yaxis() #invert the y-axis so the first row of data is at the top
    gui.show()

def isInMaze(maze,cell) :
    return (cell[0]<len(maze) and cell[1]<len(maze[0]))

def isNotWall(maze,cell) :
    return (maze[cell[0]][cell[1]]==0)

def h(cell,goal) :
    x1 = cell[0]
    y1 = cell[1]
    x2 = goal[0]
    y2 = goal[1]
    return abs(x1-x2)+abs(y1-y2)

def reconstruct_path(fromList, current) :
    total_path = [current]
    while current in fromList :
        current = fromList[current]
        total_path.append(current)
    return total_path

def bfs(maze, start, end):
    
    visited = set()
    jalur = [start]
    
    while len(jalur) != 0:
        if jalur[0] == start:
            path = [jalur.pop(0)] 
        else:
            path = jalur.pop(0)

        closedSet = path[-1]

        if closedSet == end:
            return path
        elif closedSet not in visited:
            for adjacentDirection in getAdjacentDirections(maze, visited,closedSet):
                maze[closedSet[0]][closedSet[1]]=2
                allPath = list(path)
                allPath.append(adjacentDirection)
                jalur.append(allPath)
            visited.add(closedSet)

def getAdjacentDirections(maze, visited,direction ):

    directions = list()
    node = list()
    vertical = direction[0]
    horizontal = direction[1]
    #cek direction
    directions.append((vertical-1, horizontal))  # atas
    directions.append((vertical+1, horizontal))  # bawah
    directions.append((vertical, horizontal-1))  # kiri
    directions.append((vertical, horizontal+1))  # kanan
    
    for i in directions:
        if maze[i[0]][i[1]] != 1 and i not in visited:
            node.append(i)
    return node    

def AStar(maze,start,end) :
    g = {start:0}
    f = {start:0}
    f[start] = g[start] + h(start,end)

    openSet = []
    closedSet = []

    openSet.append(start)
    fromList = {}
    all_path = []

    while (openSet) :
        currentCell = openSet[0]
        for cell in openSet :
            if (f[cell] < f[currentCell]) :
                currentCell = cell

        if (currentCell == end) :
            all_path = reconstruct_path(fromList,currentCell)
            break

        openSet.remove(currentCell)
        closedSet.append(currentCell)
        for direction in [(1,0),(0,1),(-1,0),(0,-1)] :
            temp_cell = tuple(map(operator.add,currentCell,direction))
            if (isInMaze(maze,temp_cell)) :
                if (isNotWall(maze,temp_cell)) :
                    if ((temp_cell) in closedSet) :
                        continue
                    
                    temp_g = g[currentCell] + 1
                    if (currentCell not in openSet) :
                        openSet.append(temp_cell)
                    else :
                        continue
                    fromList[temp_cell] = currentCell
                    g[temp_cell] = temp_g
                    f[temp_cell] = g[temp_cell] + h(temp_cell,end)
    print("Panjang Path :")
    print(len(all_path))
    for coor in closedSet:
        x,y = coor
        maze[x][y]=2
    for path in all_path:
        x,y = path
        maze[x][y]=3

def main() :
    maze = []
    print("---------------------")
    print("     MAZE PROBLEM    ")
    print("---------------------")
    print()
    print("> Masukkan nama file : ", end = "")
    file = input()
    print()
    readMaze(maze,file)
    print_maze(maze)
    print()
    rows = len(maze)
    cols = len(maze[0])
    for i in range(rows) :
        if (maze[i][0]==0) :
            start = (i,0)
        if (maze[i][cols-1]==0) :
            end = (i,cols-1)
    print("Metode Pencarian")
    print("1. A*Star")
    print("2. BFS")
    print("Pilih metode : ",end="")
    metode=input()
    print()
    if (metode == '1'):
        AStar(maze,start,end)
        print_maze(maze)
    elif (metode == '2'):
        peta=bfs(maze,start,end)
        for node in peta:
            maze[node[0]][node[1]]=3    
        print_maze(maze)       
main()
