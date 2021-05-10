import heapq
from queue import Queue
import numpy as np
import math
import time
import sys

# Problem
class Grid:
    def __init__(self, gridInput, rowSize=None, colSize=None,
                    transitions = ((0, 1), (0, -1), (-1, 0), (1, 0))):
        if type(gridInput) == str:
            self.grid = self.parseGridFile(gridInput)
        if type(gridInput) == list:
            self.grid = gridInput
            self.rowSize = len(gridInput)
            self.colSize = len(gridInput[0])
            self.start = (0, 0)
            self.goal = (self.rowSize-1, self.colSize-1)
        
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
            runningCost += self.grid[y][x]
        return runningCost

    def parseGridFile(self, gridFile):
        fp = open(gridFile, "r")
        # parse header
        dimensions = int(fp.readline())
        self.rowSize = dimensions
        self.colSize = dimensions
        pixelWidth = fp.readline()

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
    
    def collapseGrid(self):
        return np.array(self.grid).flatten()

# Helper class for AStar
class AStarNode:
    def __init__(self, f, g, pos, parent, depth):
        self.f = f
        self.g = g
        self.pos = pos
        self.parent = parent
        self.depth = depth

    def __repr__(self):
        return "(" + str(self.f) + ", " + str(self.pos) + ")"
    
    # For priority queue
    def __lt__(self, other):
        return self.f < other.f

    # For priority queue
    def __gt__(self, other):
        return self.f > other.f

# Algorithms
class AStar:
    def __init__(self, grid, heur):
        self.grid = grid
        self.heuristic = heur
        self.statesExplored = 0
        self.depthFound = 0
    
    def queueTransitions(self, frontier, explored, node, depth):
        for i in range(len(self.grid.transitions)):
            if self.grid.checkBounds(node.pos, self.grid.transitions[i]):
                explored += [node.pos]
                nextPos = (node.pos[0] + self.grid.transitions[i][0],
                            node.pos[1] + self.grid.transitions[i][1])
                if len([exnode for exnode in explored if exnode == nextPos]) > 0: # disallow backtracking
                    continue
                g = node.g + self.grid.pathCost([nextPos])
                if len([ennode for ennode in frontier
                        if ennode.pos == nextPos and g > ennode.g]) > 0:
                    continue
                h = self.heuristic.compute(node.pos, self.grid.goal) # calc h(x)
                f = g + h
                heapq.heappush(frontier, AStarNode(f, g, nextPos, node, depth+1))
    
    def reconstructPath(self, node):
        # reconstruct path
        path = [node.pos]
        while node.parent != None:
            node = node.parent
            path += [node.pos]
        path.reverse()
        return path

    def search(self):
        statesExplored = 0
        frontier = []
        explored = []
        heapq.heapify(frontier)
        # init frontier
        heapq.heappush(frontier, AStarNode(0, 0, self.grid.start, None, 0))
        statesExplored += 1
        # main loop
        while frontier != []:
            currentNode = heapq.heappop(frontier)
            currentDepth = currentNode.depth
            currentPos = currentNode.pos
            statesExplored += 1
            if self.grid.goal == currentPos: # goal test
                self.statesExplored = statesExplored
                self.depthFound = currentDepth
                return self.reconstructPath(currentNode)
            self.queueTransitions(frontier, explored, currentNode, currentDepth)
        return None # no solution

class DFSB:
    def __init__(self, grid, optimal=False):
        self.grid = grid
        self.statesExplored = 0
        self.depthFound = 0
        self.optimal = optimal
    
    def search(self, path=[]):
        if path == []:
            path = [self.grid.start]
        self.statesExplored += 1
        self.depthFound += 1

        if self.optimal and len(path) >= self.grid.rowSize + self.grid.colSize:
            self.depthFound -= 1
            return None
        if path[-1] == self.grid.goal: # is a solution
            return path

        for transition in self.grid.transitions:
            if self.grid.checkBounds(path[-1], transition):
                nextNode = (path[-1][0] + transition[0],
                            path[-1][1] + transition[1])
                if nextNode in path: # disallow retracing steps
                    continue
                result = self.search(path + [nextNode])
                if result != None:
                    return result
                self.depthFound -= 1
        return None # no answer in this node

class BFS:
    def __init__(self, grid):
        self.grid = grid
        self.statesExplored = 0
        self.depthFound = 0
    
    def reconstructPath(self, node):
        # reconstruct path
        path = [node[0]]
        while node[1] != None:
            node = node[1]
            path += [node[0]]
        path.reverse()
        return path
    
    def search(self):
        queue = Queue()
        queue.put((self.grid.start, None))
        explored = [self.grid.start]

        while not queue.empty():
            currentNode = queue.get()
            self.statesExplored += 1
            if currentNode[0] == self.grid.goal: # is a solution
                return self.reconstructPath(currentNode)
            for transition in self.grid.transitions:
                if self.grid.checkBounds(currentNode[0], transition):
                    nextNode = (currentNode[0][0] + transition[0],
                                currentNode[0][1] + transition[1])
                    if len([exnode for exnode in explored if exnode == nextNode]) == 0:
                        explored += [nextNode]
                        queue.put((nextNode, currentNode))
        return None # no answer in this node

class Dijkstra:
    def __init__(self, grid):
        self.grid = grid
        self.statesExplored = 0
        self.depthFound = 0
    
    def findMin(self, queue):
        minNode = (math.inf, None, None)
        for node in queue:
            if node[0] < minNode[0]:
                minNode = node
        return minNode

    def findNode(self, queue, pos):
        for node in queue:
            if node[1] == pos:
                return node
        return None

    def changeNode(self, queue, pos, dist, parent):
        for node in queue:
            if node[1] == pos:
                queue.remove(node)
                queue += [(dist, pos, parent)]
                return
        return
    
    def search(self):
        # node = (dist, position, parent)
        queue = []
        finished = []

        # init
        for j in range(self.grid.colSize):
            for i in range(self.grid.rowSize):
                if (i, j) == self.grid.start:
                    queue += [(0, (i,j), None)]
                else:
                    queue += [(math.inf, (i,j), None)]
        
        # main loop
        while queue != []:
            currentNode = self.findMin(queue)
            self.statesExplored += 1
            currentPos = currentNode[1]
            finished += [currentNode]
            queue.remove(currentNode)
            for transition in self.grid.transitions:
                if self.grid.checkBounds(currentPos, transition):
                    nextPos = (currentPos[0] + transition[0],
                               currentPos[1] + transition[1])
                    nextNode = self.findNode(queue, nextPos)
                    if(nextNode == None): # no longer in queue
                        continue
                    cost = currentNode[0] + self.grid.pathCost([currentPos, nextPos])
                    if cost < nextNode[0]:
                        self.changeNode(queue, nextPos, cost, currentPos)
        
        # reconstruct path
        node = self.findNode(finished, self.grid.goal)
        path = [node[1]]
        while node[2] != None:
            node = self.findNode(finished, node[2])
            path += [node[1]]
        path.reverse()
        
        return path

# Heuristics
class ManhattanHeuristic():
    """ Taxicab distance from goalState """
    def compute(self, currentNode, goal):
        return abs(currentNode[0] - goal[0]) + abs(currentNode[1] - goal[1])

class EuclideanHeuristic():
    """ Euclidean distance from goalState """
    def compute(self, currentNode, goal):
        return ( (currentNode[0] - goal[0])**2 + (currentNode[1] - goal[1])**2 )**0.5


if __name__ == "__main__":
    a = int(sys.argv[1])
    t = sys.argv[2]

    grid = Grid(t)
    algos = [AStar(grid, ManhattanHeuristic()), 
                DFSB(grid, optimal=True),
                BFS(grid),
                Dijkstra(grid)]
    algo = algos[a]

    start = time.time()
    path = algo.search()
    end = time.time()
    print("Path:", algo.search())
    print("Path Cost:", grid.pathCost(path))
    print("Time (s):", end - start)
    print("Time (ms):", (end - start) * 1000.0)