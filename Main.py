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
    parser.add_argument("n", help="width",
                        type=int)
    args = parser.parse_args()
    n=args.n

    # initialize training data
    print("Generating Data...")
    #gs.Initialize("Shapes", 250)
    gg.Initialize(n*200, n)
    trueGrid = pf.Grid("grid.txt")
    ground = np.array(trueGrid.collapseGrid())
    print(ground)

    # train and predict
    print("Training Model...")
    predictedGrid = ip.train(50, n, ground)
    print(predictedGrid.tolist())
    predictedGrid = pf.Grid(predictedGrid.tolist()) # wrap grid

    # pathfind using predicted grid
    print("Pathfinding...")
    algo = pf.AStar(predictedGrid, pf.EuclideanHeuristic())
    #algo = pf.Dijkstra(predictedGrid)
    start = time.time()
    path = algo.search()
    end = time.time()
    print("Time (s):", end - start)
    print("Time (ms):", (end - start) * 1000.0)
    print("Predicted Path Cost:", predictedGrid.pathCost(path))
    print("True Path Cost:", trueGrid.pathCost(path))