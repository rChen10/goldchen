#from tkinter import *
#from turtle import *
import sys
from PIL import Image,ImageDraw
import os
import random
import math

def Initialize(shape_dir):
    curr_dir=os.getcwd()
    shapes_dir=curr_dir+'\\'+shape_dir#Directory of Shape folder
    num_images=10 #number of images to draw for each category, may be replaced by a parameter as a system argument

    for root, subdirectories, files in os.walk(shapes_dir):
        for subdirectory in subdirectories:#Each folder is named the integer value for the amount of sides of the shape images it contains
            #maybe we can have 0, 1, and 2 folder names represent non polygon shapes, like a circle or an X
            num_sides=int(subdirectory)
            curr_path=(os.path.join(root, subdirectory))
            for i in range(num_images):
                DrawImage(num_sides,num_images,i,curr_path)#the image drawn will be in a file named i in curr_path

        
def DrawImage(num_sides,num_images,i,curr_path):
    n=200   
    img = Image.new("RGB", (n, n), (255, 255, 255))#Generates a 200x200 white image. Some variables might be parameterized later on
    im = ImageDraw.Draw(img)
    if num_sides>=3:#polygon
        im.regular_polygon((n/2,n/2,random.randint(math.ceil(n/4), math.floor(n/2))), num_sides, rotation=random.randint(0,math.floor(360/num_sides)), fill="#000000", outline=None)


    img.save(os.path.join(curr_path,str(i)+".png"), "PNG")#saves the image, named i, into the folder with the curr_path directory


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Error: invalid arguments for GenerateShapes.py!')
        exit(-1)
    shapes_dir=sys.argv[1]
    Initialize(shapes_dir)