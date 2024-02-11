from js import File, Uint8Array, window, navigator
import js
from io import BytesIO
import json
import sys
import os
from pathlib import Path
from pyodide.http import pyfetch
import asyncio
from PIL import Image
import pyperclip

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


async def draw_image():
    img_html = js.document.getElementById("preview")

    image1 = get_square()
    array_buf = Uint8Array.new(await image1.arrayBuffer())
    bytes_list = bytearray(array_buf)
    my_bytes = BytesIO(bytes_list) 
    my_image = Image.open(my_bytes)

    # image2 = get_triangle()
    # img2Bytes = BytesIO()
    # image2.save(img2Bytes, format='PNG')
    # image1.paste(image2, (400,200))

    # image1.save(image1, format='PNG')
    image2 = get_triangle()
    array_buf = Uint8Array.new(await image2.arrayBuffer())
    bytes_list = bytearray(array_buf)
    my_bytes2 = BytesIO(bytes_list) 
    my_image2 = Image.open(my_bytes2)
    my_image.paste(my_image2, (0,0), mask = my_image2)

    my_stream = BytesIO()
    my_image.save(my_stream, format="PNG")
    image_file = File.new([Uint8Array.new(my_stream.getvalue())], image1.name, {type: "image/png"})

    img_html.classList.remove("loading")
    img_html.classList.add("ready")
    
    img_html.src = window.URL.createObjectURL(image_file)

    #canvas.style["display"] = "block"

def get_square():
    image_file = get_image_from_pyodide(dictSquare[str(squareIndex)],"square.png")
    return image_file

def get_triangle():
    image_file = get_image_from_pyodide(dictTriangle[str(triangleIndex)],"triangle.png")
    return image_file

def get_image_from_pyodide(path, name):
    f = open(path, 'rb')
    image_file = File.new([Uint8Array.new(f.read())], name, {"type": "image/png"})
    return image_file

# Buttons
async def squareMinus(ev):
    global squareIndex
    squareIndex = squareIndex - 1
    if squareIndex < 0 :
        squareIndex = len(dictSquare) - 1 
    displayIndex("square")
    await draw_image()
    
async def squarePlus(ev):
    global squareIndex
    squareIndex = squareIndex + 1
    if squareIndex >= len(dictSquare) :
        squareIndex = 0
    displayIndex("square")
    await draw_image()

async def triangleMinus(ev):
    global triangleIndex
    triangleIndex = triangleIndex - 1
    if triangleIndex < 0 :
        triangleIndex = len(dictSquare) - 1 
    displayIndex("triangle")
    await draw_image()

async def trianglePlus(ev):
    global triangleIndex
    triangleIndex = triangleIndex + 1
    if triangleIndex >= len(dictTriangle) :
        triangleIndex = 0
    displayIndex("triangle")
    await draw_image()

def copy_seed(ev):
    global triangleIndex, dictTriangle
    global squareIndex, dictSquare

    seed = "square-" + dictSquare[str(squareIndex)].replace("/assets/square/","").replace(".png","")+ ";"
    seed = seed + "triangle-" + dictTriangle[str(triangleIndex)].replace("/assets/triangle/","").replace(".png","")+";"
    
    navigator.clipboard.writeText(seed)

# display index
def displayIndex(shape):
    if shape == "square":
        textIndex = js.document.getElementById("squareIndex") 
        textIndex.innerText = dictSquare[str(squareIndex)].replace("/assets/square/","").replace(".png","")
    elif shape == "triangle":
        textIndex = js.document.getElementById("triangleIndex") 
        textIndex.innerText = dictTriangle[str(triangleIndex)].replace("/assets/triangle/","").replace(".png","")

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
    displayIndex("square")
    displayIndex("triangle")
    await draw_image()

loop = asyncio.get_event_loop()
loop.run_until_complete(main())