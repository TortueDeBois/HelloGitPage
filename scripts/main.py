from pyweb import pydom
from pyscript import when
from pyodide.ffi import to_js
import asyncio
from js import (
    CanvasRenderingContext2D as Context2d,
    ImageData,
    Uint8ClampedArray,
    document,
    console
)

width, height = 600, 600

is_selecting = False
init_sx, init_sy = None, None
sx, sy = None, None

projectName = "\\HelloGitPage"
data = ["\\square\\red.png","\\square\\blue.png", "\\triangle\\green.png", "\\triangle\\yellow.png"]

dictSquare = {}
squareIndex = 0
dictTriangle = {}
triangleIndex = 0

def initDict(path):
    dictTemp = {}
    i = 0
    for value in data:
        if path in value:
            dictTemp[i] = value.replace("\\"+path+"\\","")
            i = i + 1
    return dictTemp


def prepare_canvas(width: int, height: int, canvas: pydom.Element) -> Context2d:
    ctx = canvas._js.getContext("2d")

    canvas.style["width"] = f"{width}px"
    canvas.style["height"] = f"{height}px"

    canvas._js.width = width
    canvas._js.height = height

    ctx.clearRect(0, 0, width, height)

    return ctx

def draw_canvas(width, height) -> None:
    canvas = pydom["canvas"][0]

    canvas.style["display"] = "none"

    ctx = prepare_canvas(width, height, canvas)

    draw_square(ctx)

    canvas.style["display"] = "block"

def draw_square(ctx):
    key = squareIndex
    image = document.createElement('img')
    image.src = projectName + "\\assets\\square\\" + dictSquare[key]

    draw_image(ctx,image)

def draw_image(ctx, image):
    ctx.drawImage(image, 0, 0, 10, 10, 0, 0, width, height)

def main():
    dictSquare = initDict("square")
    dictTriangle = initDict("triangle")
    draw_canvas(width, height)

main()