import argparse
from PIL import Image,ImageDraw
import random
import math


def Initialize(grid_size,step_count):
    img = Image.new(mode='RGB', size=(grid_size, grid_size), color="#ffffff")

    im = ImageDraw.Draw(img)#object to be drawn on, affecting image
    x_start = 0
    x_end = img.width
    y_start = 0
    y_end = img.height
    step_size = int(img.width / step_count)

    for x in range(0, img.width, step_size):#draws vertical lines
        line = ((x, y_start), (x, y_end)) # first parameter is starting coordinate, second is end coordinate
        im.line(line, fill="#7f7f7f")#draws a grey line 

    for y in range(0, img.height, step_size):#draws horizontal lines
        line = ((x_start, y), (x_end, y))
        im.line(line, fill="#7f7f7f")

    img.save("grid.png", "PNG")#saves the image, later on will add code to draw shapes in each cell

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("grid_size", help="width and height of the grid in pixels",
                        type=int)
    parser.add_argument("step_count", help="how many cells each row/column should have",
                        type=int)
    args = parser.parse_args()
    grid_size=args.grid_size
    step_count = args.step_count
    Initialize(grid_size,step_count)