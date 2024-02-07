import js
import json
import sys
import os
from pathlib import Path

width, height = 400, 200

is_selecting = False
init_sx, init_sy = None, None
sx, sy = None, None

projectName = "\\HelloGitPage"
# data = ["square\\red.png","square\\blue.png", "triangle\\green.png", "triangle\\yellow.png"]

"""
Récupérer toutes les imgs. Selon la nomenclature:
$path\\<folder>\\<file>
"""
data = []
for f in os.listdir(str(Path.cwd()) + "\\assets\\"):
    for file in os.listdir(str(Path.cwd()) + "\\assets\\" + f + "\\"):
        data.append(f + "\\" + file) #Trouver une alternativeà "append" car risque d'explosion en compléxité (temps ET mémoire)
print(data)

dictSquare = {}
squareIndex = 0
dictTriangle = {}
triangleIndex = 0

def initDict(path):
    dictTemp = {}
    i = 0
    for value in data:
        if path in value :
            dictTemp[str(i)] = value
            i = i + 1
    return dictTemp


def prepare_canvas(width, height, canvas):
    ctx = canvas.getContext("2d")

    #canvas.style["width"] = f"{width}px"
    #canvas.style["height"] = f"{height}px"

    #canvas._js.width = width
    #canvas._js.height = height

    ctx.imageSmoothingEnabled = False

    ctx.clearRect(0, 0, width, height)

    return ctx

def draw_canvas(width, height):
    canvas = js.document.getElementById("preview")

    ctx = prepare_canvas(width, height, canvas)
    
    draw_square(ctx)
    draw_triangle(ctx)

    ctx.fill()

    #canvas.style["display"] = "block"

def draw_square(ctx):
    image = js.document.createElement('img')
    image.src = projectName + "\\assets\\" + dictSquare[str(squareIndex)]
    draw_image(ctx, image)

def draw_triangle(ctx):
    image = js.document.createElement('img')
    image.src = projectName + "\\assets\\" + dictTriangle[str(triangleIndex)]
    draw_image(ctx, image)

def draw_image(ctx, image):
    ctx.drawImage(image, 0, 0, 40, 20, 0, 0, width, height)

# Buttons
def squareMinus(ev):
    global squareIndex
    squareIndex = squareIndex - 1
    if squareIndex < 0 :
        squareIndex = len(dictSquare) - 1 
    displayIndex("square")
    draw_canvas(width,height)
    
def squarePlus(ev):
    global squareIndex
    squareIndex = squareIndex + 1
    if squareIndex >= len(dictSquare) :
        squareIndex = 0
    displayIndex("square")
    draw_canvas(width,height)

def triangleMinus(ev):
    global triangleIndex
    triangleIndex = triangleIndex - 1
    if triangleIndex < 0 :
        triangleIndex = len(dictSquare) - 1 
    displayIndex("triangle")
    draw_canvas(width,height)

def trianglePlus(ev):
    global triangleIndex
    triangleIndex = triangleIndex + 1
    if triangleIndex >= len(dictTriangle) :
        triangleIndex = 0
    displayIndex("triangle")
    draw_canvas(width,height)

# display index
def displayIndex(shape):
    if shape == "square":
        textIndex = js.document.getElementById("squareIndex") 
        textIndex.innerText = dictSquare[str(squareIndex)].replace("square\\","")
    elif shape == "triangle":
        textIndex = js.document.getElementById("triangleIndex") 
        textIndex.innerText = dictTriangle[str(triangleIndex)].replace("triangle\\","")

def main():
    draw_canvas(width, height)
    displayIndex("square")
    displayIndex("triangle")

dictSquare = initDict("square")
dictTriangle = initDict("triangle")
main()