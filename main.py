from copy import deepcopy
from random import choice

class Grid:
    def __init__(self, size=4)->list[list[str]]:
        self.size = size
        self.grid = [['.' for i in range(size)] for i in range(size)]

    def spawnNumber(self):
        if len(self.getEmptyBox()) > 0:
            self.setBoxValue(choice(self.getEmptyBox()), "2")

    def moveGrid(self, mov: tuple):
        newGrid = deepcopy(self.grid)
        for i in self.getGridPathI(mov):
            for j in self.getGridPathJ(mov, i):
                if not self.isEmptyBox(newGrid[i][j]):
                    if mov[0] != 0 and -1<i+mov[0]<self.size:
                        self.moveColumn(newGrid, mov, i, j)
                    elif mov[1] != 0 and -1<j+mov[1]<self.size:
                        self.moveLine(newGrid, mov, i, j)                        
        self.grid = newGrid

    def moveColumn(self, newGrid: list, mov: tuple, i: int, j: int)->list:
        liste, nextI = self.getColumn(j, newGrid), i
        for n in self.getMoveRange(mov, liste, i):
            if not self.isEmptyBox(liste[n]):
                if liste[n] == liste[i]:
                    nextI = n   
                break
            nextI = n
        newGrid[i][j], newGrid[nextI][j] = '.', self.getNewBoxValueColumn(newGrid, i, j, nextI)
        return newGrid

    def moveLine(self, newGrid: list, mov: tuple, i: int, j: int)->list:
        liste, nextJ = self.getLine(i, newGrid), j
        for n in self.getMoveRange(mov, liste, j):
            if not self.isEmptyBox(liste[n]):
                if liste[n] == liste[j]:
                    nextJ = n
                break                
            nextJ = n
        newGrid[i][j], newGrid[i][nextJ] = '.', self.getNewBoxValueLine(newGrid, i, j, nextJ)
        return newGrid    

    def isEmptyBox(self, value: str)->bool:
        return value == '.'

    def setBoxValue(self, pos: tuple, value: str):
        self.grid[pos[0]][pos[1]] = value

    def getNewBoxValueColumn(self, newGrid: list, i: int, j: int, nextI: int):
        som = 0
        if nextI != i:
            som = self.getIntBoxValue((nextI,j),newGrid)
        return str(self.getIntBoxValue((i,j),newGrid)+som)

    def getNewBoxValueLine(self, newGrid: list, i: int, j: int, nextJ: int):
        som = 0
        if nextJ != j:
            som = self.getIntBoxValue((i,nextJ),newGrid)
        return str(self.getIntBoxValue((i,j),newGrid)+som)

    def getGridPathI(self, mov: tuple)->range:
        return range(len(self.grid)-1,-1,-1) if mov[0]==1 else range(len(self.grid))

    def getGridPathJ(self, mov: tuple, i: int)->range:
        return range(len(self.grid[i])-1,-1,-1) if mov[1]==1 else range(len(self.grid[i]))

    def getMoveRange(self, mov: tuple, liste: list, i)->range:
        return range(i+1, len(liste)) if mov[0]==1 or mov[1]==1 else range(i-1, -1, -1)

    def getEmptyBox(self)->list:
        return [(i,j) for i in range(len(self.grid)) for j in range(len(self.grid[i])) if self.grid[i][j] == "."]

    def getIntBoxValue(self, pos: tuple, grid: list)->int:
        return int(grid[pos[0]][pos[1]]) if grid[pos[0]][pos[1]] != '.' else 0

    def getLine(self, i: int, grid: list[list[str]])->list[str]:
        return grid[i]

    def getColumn(self, j: int, grid: list[list[str]])->list[str]:
        return [grid[i][j] for i in range(len(grid))]

    def __str__(self)->None:
        print('\n')
        return '\n'.join(''.join(str(i).center(5) for i in row) for row in self.grid)


grid = Grid()
grid.spawnNumber()
print(grid, "spawn")

while True:
    s = input("Play: ")
    match s:
        case "z": m=(-1,0)
        case "s": m=(1,0)
        case "q": m=(0,-1)
        case "d": m=(0,1)
        case "p": break  
    grid.moveGrid(m)
    print(grid, "move")
    grid.spawnNumber()
    print(grid, "spawn")