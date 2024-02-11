from js import File, Uint8Array, window
import js
import json
import sys
import os
from pathlib import Path
from pyodide.http import pyfetch
import asyncio
from PIL import Image

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

    for f in os.listdir(path):
        dictTemp[str(i)] = path + "/" + f
        i = i + 1
    return dictTemp


def draw_image():
    img_html = js.document.getElementById("preview")

    image1 = draw_square()
    img = image1

    image2 = draw_triangle()
    img.paste(image2, (400,200))
    #to do here combinaison d'image voir pillow (pil)

    img_html.src = img.src

    #canvas.style["display"] = "block"

def draw_square():
    image_file = get_image_from_pyodide(dictSquare[str(squareIndex)],"square.png")
    image = js.document.createElement('img')
    image.src = window.URL.createObjectURL(image_file)
    return image

def draw_triangle():
    image_file = get_image_from_pyodide(dictTriangle[str(triangleIndex)],"triangle.png")
    image = js.document.createElement('img')
    image.src = window.URL.createObjectURL(image_file)
    return image

def get_image_from_pyodide(path, name):
    f = open(path, 'rb')
    image_file = File.new([Uint8Array.new(f.read())], name, {"type": "image/png"})
    return image_file

# Buttons
def squareMinus(ev):
    global squareIndex
    squareIndex = squareIndex - 1
    if squareIndex < 0 :
        squareIndex = len(dictSquare) - 1 
    displayIndex("square")
    draw_image()
    
def squarePlus(ev):
    global squareIndex
    squareIndex = squareIndex + 1
    if squareIndex >= len(dictSquare) :
        squareIndex = 0
    displayIndex("square")
    draw_image()

def triangleMinus(ev):
    global triangleIndex
    triangleIndex = triangleIndex - 1
    if triangleIndex < 0 :
        triangleIndex = len(dictSquare) - 1 
    displayIndex("triangle")
    draw_image()

def trianglePlus(ev):
    global triangleIndex
    triangleIndex = triangleIndex + 1
    if triangleIndex >= len(dictTriangle) :
        triangleIndex = 0
    displayIndex("triangle")
    draw_image()

# display index
def displayIndex(shape):
    if shape == "square":
        textIndex = js.document.getElementById("squareIndex") 
        textIndex.innerText = dictSquare[str(squareIndex)].replace("/assets/square/","")
    elif shape == "triangle":
        textIndex = js.document.getElementById("triangleIndex") 
        textIndex.innerText = dictTriangle[str(triangleIndex)].replace("/assets/triangle/","")

async def init_assets():
    global data
    path = "/assets"
    os.mkdir(path) 

    for info in data:
        path = "/assets/" + info.split('\\')[0]

        if not os.path.exists(path):
            os.mkdir(path) 

        url = "https:\\\\tortuedebois.github.io" + projectName + "\\assets\\" + info
        response = await pyfetch(url)

        with open("/assets/" + info.replace("\\","/"), mode="wb") as f:
            f.write(await response.bytes())


    # files = os.listdir('/assets')
    # for file in files:
    #     js.console.log(file)

    #     for f in os.listdir('/assets/' + file):
    #         js.console.log("\t" + f)


def init_data():
    """
    Récupérer toutes les imgs. Selon la nomenclature:
    $path\\<folder>\\<file>
    """
    # data = []
    # for f in os.listdir(str(Path.cwd()) + "/assets/"):
    #     for file in os.listdir(str(Path.cwd()) + "/assets/" + f + "/"):
    #         data.append(f + "/" + file) #Trouver une alternativeà "append" car risque d'explosion en compléxité (temps ET mémoire)
    # print(data)

    global dictSquare, dictTriangle

    files = os.listdir('/assets')
    for file in files:
        if file == "square":
            dictSquare = initDict("/assets/" + file)
        elif file == "triangle":
            dictTriangle = initDict("/assets/" + file)

async def main():
    await init_assets()
    init_data()
    draw_image()
    displayIndex("square")
    displayIndex("triangle")


loop = asyncio.get_event_loop()
loop.run_until_complete(main())