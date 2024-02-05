import js
import json
import sys

width, height = 400, 200

is_selecting = False
init_sx, init_sy = None, None
sx, sy = None, None

projectName = "\\HelloGitPage"
data = ["square\\red.png","square\\blue.png", "triangle\\green.png", "triangle\\yellow.png"]

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

    #canvas.style["display"] = "none"

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



def main():
    draw_canvas(width, height)


dictSquare = initDict("square")
dictTriangle = initDict("triangle")
main()