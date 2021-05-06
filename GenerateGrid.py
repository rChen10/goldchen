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

    shapes=""#string will be represent grid structure

    for y in range(0, img.height, step_size):
        for x in range(0, img.width, step_size):
            if(x==0 and y==0):
                #draw agent
                im.ellipse((step_size/4, step_size/4, 3*step_size/4, 3*step_size/4), fill="#ff0000", outline=None)
                shapes="0,"#0 is agent cell
            elif(x==(img.width-step_size) and y==(img.height-step_size)):
                #draw goal
                im.ellipse((img.width-3*step_size/4, img.height-3*step_size/4, img.width-step_size/4, img.height-step_size/4), fill="#00ff00", outline=None)
                shapes+="1,"#1 is goal cell
            else:
                num_sides=random.randint(3,8)#would have to manually change this in the code if we will be generating different kinds of shapes
                shapes+=str(num_sides)+","
                im.regular_polygon((step_size/2+x,step_size/2+y,random.randint(math.ceil(step_size/4), math.floor(step_size/2))), num_sides, rotation=random.randint(0,math.floor(360/num_sides)), fill="#000000", outline=None)
        shapes=shapes[:-1]+'\n'
    shapes=str(grid_size)+'\n'+shapes
    shapes=str(step_count)+'\n'+shapes[:-1]
    f = open("grid.txt", "w")
    f.write(shapes)#file format in readme

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