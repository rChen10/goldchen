import GenerateGrid as gg
import GenerateShapes as gs
import ImageProcess as ip
import PathFind as pf
import numpy as np
import time
import math
import argparse

if __name__ == "__main__":
    # parse agrs
    parser = argparse.ArgumentParser()
    parser.add_argument("n", help="height and width of grid in cell count",
                        type=int)
    parser.add_argument("samples", help="number of samples per shape",
                        type=int)
    parser.add_argument("scale", help="scale for the costs",
                        type=int)
    args = parser.parse_args()
    n=args.n
    samples=args.samples
    cscale=args.scale

    # initialize training data
    print("Generating Data...")
    gs.Initialize("Shapes", samples)
    gg.Initialize(n*200, n)
    trueGrid = pf.Grid("grid.txt", impassable=[7])
    ground = np.array(trueGrid.collapseGrid())

    # train and predict
    print("Training Model...")
    predictedGrid = ip.train(samples, n, ground)
    predictedGrid = pf.Grid(predictedGrid.tolist(), scale=cscale, impassable=[7]) # wrap grid
    trueGrid.scaleGrid(cscale)

    # pathfind using predicted grid
    print("Pathfinding...")
    algos1 = [pf.AStar(predictedGrid, pf.ManhattanHeuristic()), 
                pf.AStar(predictedGrid, pf.EuclideanHeuristic()), 
                pf.Dijkstra(predictedGrid),
                pf.DFSB(predictedGrid),
                pf.BFS(predictedGrid),
                pf.GreedyDFS(predictedGrid)]
    algos2 = [pf.AStar(trueGrid, pf.ManhattanHeuristic()),
                pf.AStar(trueGrid, pf.EuclideanHeuristic()),
                pf.Dijkstra(trueGrid),
                pf.DFSB(trueGrid),
                pf.BFS(trueGrid),     
                pf.GreedyDFS(trueGrid)]
    algoNames = ["A* (Manhattan Heuristic)", "A* (Euclidean Heuristic)", "Dijkstra", "DFSB", "BFS", "GreedyDFS"]
    
    # open file for logging
    fp1 = open("predlog.csv", "w")
    fp2 = open("truelog.csv", "w")
    fps = [fp1, fp2]
    algosList = [algos1, algos2]

    # pathfind for each algorithm
    for j in range(2):
        fp = fps[j]
        algos = algosList[j]
        print("Algorithm,Size,Samples,Time,States Explored,Predicted Path Cost,True Path Cost", file=fp)
        if j == 0:
            print("---Predicted Grid")
        if j == 1:
            print("---True Grid")
        for i in range(len(algos)):
            algo = algos[i]
            print(algoNames[i], ":")
            if i == 3 and n > 10:
                print("DFSB can't finish within reasonable time")
                continue
            start = time.time()
            path = algo.search()
            end = time.time()
            if path == None:
                print("No solution!")
                break
            ppc = predictedGrid.pathCost(path)
            tpc = trueGrid.pathCost(path, warn=True)
            ex = algo.statesExplored
            print("Time (s):", end - start)
            print("Time (ms):", (end - start) * 1000.0)
            print("States Explored:", ex)
            print("Predicted Path Cost:", ppc)
            print("True Path Cost:", tpc)

            print("%s,%d,%d,%f,%d,%d,%d" % 
                    (algoNames[i], n, samples, end-start, ex, ppc, tpc), file=fp)

    for fp in fps:
        fp.close()