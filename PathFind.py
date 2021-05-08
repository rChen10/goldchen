from queue import PriorityQueue
import functools
import math

# Problem
class Grid:
    def __init__(self, gridFile, rowSize=None, colSize=None,
                    transitions = ((0, 1), (0, -1), (-1, 0), (1, 0))):
        self.grid = self.parseGridFile(gridFile)
        self.transitions = transitions
        if rowSize != None:
            self.rowSize = rowSize
        if colSize != None:
            self.colSize = colSize
    
    def checkBounds(self, node, transition):
        newX = node[0] + transition[0]
        newY = node[1] + transition[1]
        if newX >= self.rowSize or newX < 0:
            return False
        if newY >= self.colSize or newY < 0:
            return False
        return True
    
    def pathCost(self, path): # potentialy replace with dynamic programming later
        runningCost = 0
        for node in path:
            x, y = node
            runningCost += self.grid[x][y]
        return runningCost

    def parseGridFile(self, gridFile):
        fp = open(gridFile, "r")
        # parse header
        dimensions = int(fp.readline())
        self.rowSize = dimensions
        self.colSize = dimensions
        idk = fp.readline()

        # parse grid
        grid = [] 
        for i in range(dimensions):
            line = fp.readline()
            row = line.split(",")
            row = [int(cost) for cost in row]
            grid += [row]

        # find start & goal
        for i in range(len(grid)):
            row = grid[i]
            for j in range(len(row)):
                if grid[i][j] == 0:
                    self.start = (i, j)
                if grid[i][j] == 1:
                    self.goal = (i, j)
        return grid

# Algorithms
class AStar:
    def __init__(self, grid, heur):
        self.grid = grid
        self.heuristic = heur
    
    def queueTransitions(self, frontier, path, depth):
        for i in range(len(self.grid.transitions)):
            if self.grid.checkBounds(path[-1], self.grid.transitions[i]):
                nextNode = (path[-1][0] + self.grid.transitions[i][0],
                            path[-1][1] + self.grid.transitions[i][1])
                if nextNode not in path: # disallow backtracking
                    h = self.heuristic.compute(path, self.grid.goal) # calc h(x)
                    item = path + [nextNode]
                    f = self.grid.pathCost(item) + h
                    frontier.put((f, item, depth+1))

    def search(self):
        path = [] # aka current state
        path += [grid.start]
        statesExplored = 0
        frontier = PriorityQueue()
        # init frontier
        self.queueTransitions(frontier, path, 0)
        statesExplored += 1
        # main loop
        while not frontier.empty():
            currentItem = frontier.get()
            currentDepth = currentItem[2]
            currentPath = currentItem[1]
            statesExplored += 1
            if self.grid.goal == currentPath[-1]: # goal test
                self.statesExplored = statesExplored
                self.depthFound = currentDepth
                return currentPath
            self.queueTransitions(frontier, currentPath, currentDepth)
        return None # no solution

# Heuristics
class ManhattanHeuristic():
    """ Taxicab distance from goalState """
    def compute(self, path, goal):
        currentNode = path[-1]
        return abs(currentNode[0] - goal[0]) + abs(currentNode[1] - goal[1])

if __name__ == "__main__":
    grid = Grid("grid.txt")
    algo = AStar(grid, ManhattanHeuristic())
    print(algo.search())