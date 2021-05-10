import GenerateGrid as gg
import GenerateShapes as gs
import ImageProcess as ip
import PathFind as pf
import numpy as np
import time
import argparse

if __name__ == "__main__":
    # parse agrs
    parser = argparse.ArgumentParser()
    parser.add_argument("n", help="height and width of grid",
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
    #gs.Initialize("Shapes", 250)
    #gg.Initialize(n*200, n)
    trueGrid = pf.Grid("grid.txt", impassable=[7])
    ground = np.array(trueGrid.collapseGrid())

    # train and predict
    print("Training Model...")
    predictedGrid = ip.train(samples, n, ground)
    predictedGrid = pf.Grid(predictedGrid.tolist(), scale=cscale, impassable=[7]) # wrap grid
    trueGrid.scaleGrid(cscale)

    # pathfind using predicted grid
    print("Pathfinding...")
    algos = [pf.AStar(predictedGrid, pf.ManhattanHeuristic()), 
                pf.AStar(predictedGrid, pf.EuclideanHeuristic()), 
                pf.Dijkstra(predictedGrid),
                pf.DFSB(predictedGrid, optimal=True),
                pf.BFS(predictedGrid)]
    algoNames = ["A* (Manhattan Heuristic)", "A* (Euclidean Heuristic)", "Dijkstra", "DFSB", "BFS"]
    
    # open file for logging
    fp = open("testlog.csv", "w")
    print("Algorithm,Size,Samples,Time,States Explored,Predicted Path Cost,True Path Cost", file=fp)

    # pathfind for each algorithm
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
        tpc = trueGrid.pathCost(path)
        ex = algo.statesExplored
        print("Time (s):", end - start)
        print("Time (ms):", (end - start) * 1000.0)
        print("States Explored:", ex)
        print("Predicted Path Cost:", ppc)
        print("True Path Cost:", tpc)

        print("%s,%d,%d,%f,%d,%d,%d" % 
                (algoNames[i], n, samples, end-start, ex, ppc, tpc), file=fp)

    fp.close()