import GenerateGrid as gg
import GenerateShapes as gs
import ImageProcess as ip
import PathFind as pf

if __name__ == "__main__":
    # initialize training data
    print("Generating Data...")
    gs.Initialize("Shapes", 250)
    gg.Initialize(2000, 10)
    trueGrid = pf.Grid("grid.txt")
    ground = trueGrid.collapseGrid()

    # train and predict
    print("Training Model...")
    predictedGrid = ip.train(250, 10, ground)
    predictedGrid = pf.Grid(predictedGrid) # wrap grid

    # pathfind using predicted grid
    print("Pathfinding...")
    algo = pf.AStar(pf.Grid, pf.ManhattanHeuristic())
    path = algo.search()
    print("Predicted Path Cost:", predictedGrid.pathCost(path))
    print("True Path Cost:", trueGrid.pathCost(path))
    pass