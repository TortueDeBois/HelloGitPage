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
from PIL.PngImagePlugin import PngInfo

width, height = 400, 200

is_selecting = False
init_sx, init_sy = None, None
sx, sy = None, None

projectName = "/HelloGitPage"
data = ["square/red.png","square/blue.png", "triangle/green.png", "triangle/yellow.png"]

dictSquare = {}
squareIndex = 0
dictTriangle = {}
triangleIndex = 0

previewImage = None

def initDict(path):
    dictTemp = {}
    i = 0

    for f in os.listdir(path):
        dictTemp[str(i)] = path + "/" + f
        i = i + 1
    return dictTemp

async def draw_image():
    global previewImage

    img_html = js.document.getElementById("preview")

    metadata = set_metadata()

    image1 = get_square()
    array_buf = Uint8Array.new(await image1.arrayBuffer())
    bytes_list = bytearray(array_buf)
    my_bytes = BytesIO(bytes_list) 
    my_image = Image.open(my_bytes)

    image2 = get_triangle()
    array_buf = Uint8Array.new(await image2.arrayBuffer())
    bytes_list = bytearray(array_buf)
    my_bytes2 = BytesIO(bytes_list) 
    my_image2 = Image.open(my_bytes2)
    my_image.paste(my_image2, (0,0), mask = my_image2)

    my_stream = BytesIO()
    my_image.save(my_stream, format="PNG", pnginfo=metadata)
    image_file = File.new([Uint8Array.new(my_stream.getvalue())], image1.name, {type: "image/png"})
    previewImage = my_image

    img_html.classList.remove("loading")
    img_html.classList.add("ready")
    
    img_html.src = window.URL.createObjectURL(image_file)

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

def set_metadata():
    metadata = PngInfo()
    metadata.add_text("Original_Creator", "Limezu")
    return metadata

def get_seed():
    global triangleIndex, dictTriangle
    global squareIndex, dictSquare

    seed = "square-" + dictSquare[str(squareIndex)].replace("/assets/square/","").replace(".png","") + ";"
    seed = seed + "triangle-" + dictTriangle[str(triangleIndex)].replace("/assets/triangle/","").replace(".png","") + ";"

    return seed

def change_seed_in_seed_area():
    seed = get_seed()
    textElement = js.document.getElementById("seedArea") 
    textElement.innerText = seed

# Buttons
async def squareMinus(ev):
    global squareIndex
    squareIndex = squareIndex - 1
    if squareIndex < 0 :
        squareIndex = len(dictSquare) - 1 
    displayIndex("square")
    await draw_image()
    change_seed_in_seed_area()
    
async def squarePlus(ev):
    global squareIndex
    squareIndex = squareIndex + 1
    if squareIndex >= len(dictSquare) :
        squareIndex = 0
    displayIndex("square")
    await draw_image()
    change_seed_in_seed_area()

async def triangleMinus(ev):
    global triangleIndex
    triangleIndex = triangleIndex - 1
    if triangleIndex < 0 :
        triangleIndex = len(dictSquare) - 1 
    displayIndex("triangle")
    await draw_image()
    change_seed_in_seed_area()

async def trianglePlus(ev):
    global triangleIndex
    triangleIndex = triangleIndex + 1
    if triangleIndex >= len(dictTriangle) :
        triangleIndex = 0
    displayIndex("triangle")
    await draw_image()
    change_seed_in_seed_area()

def copy_seed(ev):
    seed = get_seed()

    navigator.clipboard.writeText(seed)

def dl_preview(ev):
    global previewImage

    metadata = set_metadata()
    previewImage = previewImage.resize((200,100), Image.BILINEAR)
    my_stream = BytesIO()
    previewImage.save(my_stream, format="PNG", pnginfo=metadata)
    image_file = File.new([Uint8Array.new(my_stream.getvalue())], "unused_file_name.png", {type: "image/png"})
    url = js.URL.createObjectURL(image_file)

    hidden_a = js.document.createElement('a')
    hidden_a.setAttribute('href', url)
    hidden_a.setAttribute('download', "new_image.png")
    hidden_a.click()

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
        path = "/assets/" + info.split('/')[0]

        if not os.path.exists(path):
            os.mkdir(path) 

        url = "https://tortuedebois.github.io" + projectName + "/assets/" + info
        response = await pyfetch(url)

        with open("/assets/" + info, mode="wb") as f:
            f.write(await response.bytes())


    # files = os.listdir('/assets')
    # for file in files:
    #     js.console.log(file)

    #     for f in os.listdir('/assets/' + file):
    #         js.console.log("\t" + f)

def init_data():
    """
    Récupérer toutes les imgs. Selon la nomenclature:
    $path/<folder>/<file>
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
    change_seed_in_seed_area()

loop = asyncio.get_event_loop()
loop.run_until_complete(main())