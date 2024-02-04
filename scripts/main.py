from pyweb import pydom
from js import (
    CanvasRenderingContext2D as Context2d,
    ImageData,
    Uint8ClampedArray,
    console
)

projectName = "\\HelloGitPage"
canvas = document["preview"]
ctx = canvas.getContext("2d")
ctx.imageSmoothingEnabled = False
data = ["\\square\\red.png","\\square\\blue.png", "\\triangle\\green.png", "\\triangle\\yellow.png"]

dictSquare = {}
squareIndex = 0
dictTriangle = {}
triangleIndex = 0