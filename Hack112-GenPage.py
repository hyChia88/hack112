from cmu_graphics import *
from PIL import ImageGrab
from PIL import Image
from tkinter import filedialog
import tkinter as tk
import os

def onAppStart(app):
    app.width = 1000
    app.height = 600
    
    # UI Properties===========================================
    # Initialize images
    app.imageIn = None
    app.imageOut = None
    app.showImageIn = False
    # catch error block
    try:
        if os.path.exists('imageOut.png'):
            app.imageOut = 'imageOut.png'
        else:
            print("Warning: imageOut.png not found")
            app.imageOut = None  # or provide a default image
    except Exception as e:
        print(f"Error loading image: {e}")

    app.frameX1 = 90
    app.frameX2 = 510
    app.frameY = 70
    
    # the Icon
    app.iconPath = ['brush.png','shapes.png','eraser.png','import.png','reset.png']
    app.iconLabel = ['Brush', 'Shape', 'Erase', 'Import', 'Reset']
    
    # Button properties
    app.buttonSize = 20
    app.gapX = 145
    app.buttonStartX = 110  # Starting X position for buttons
    app.buttonColor = ['green','red','brown','black','grey']
    app.buttonY = 500   # Starting Y position for buttons
    app.borderW = 1
    
    # img size
    app.imageSize = 400
    
    # Store button positions for click detection
    app.colorButtons = []
    app.iconButtons = []
    
    # Initialize svae button
    app.saveButton = {
        'x': app.buttonStartX + (app.gapX * 5),  # Position after other buttons
        'y': app.buttonY,
        'width': 60,
        'height': 60
    }
    app.showMessage = True
    app.messageText = ''
    app.messageTimer = 0
    
    # Initialize color buttons (top row)
    for i in range(5):
        app.colorButtons.append({
            'x': app.buttonStartX + (app.gapX * i),
            'y': app.buttonY,
            'type': 'color',
            'color': app.buttonColor[i]
        })
    
    # Initialize icon buttons (bottom row)
    for i in range(5):
        app.iconButtons.append({
            'x': app.buttonStartX + (app.gapX * i),
            'y': app.buttonY + app.buttonSize * 2,
            'type': 'icon',
            'icon': app.iconPath[i],
            'label': app.iconLabel[i]
        })
    
    # Drawing Properties==========================================
    app.toolTypes = {
        'Brush': {'icon': 'brush.png'},
        'Shape': {'icon': 'shapes.png'},
        'Erase': {'icon': 'eraser.png'},
        'Import': {'icon': 'import.png'},
        'Reset': {'icon': 'reset.png'}
    }
    app.currentTool = 'Shape'  # default tool
    app.isBrushMode = False    # keep for compatibility
    app.isErasing = False      # keep for compatibility
    app.isDrawingVolume = True
    app.reset = False
    
    app.shapes = []
    app.currentShape = []
    app.canvasClicks = 0
    app.colors = []
    app.currentColor = 'black'
    app.bx, app.by = None, None
    app.brushLocations = []
    app.stepsPerSecond = 3 # steps count for Brush & refresh, keep reading imageOut.png

    app.refreshCount = 0  # Counter for number of refreshes
    app.stepCount = 0     # Counter for steps (to track 3 seconds)
    
    app.importFilePathList = []  # Initialize empty list for imported file paths
    app.currentImageIndex = 0 

def saveCanvasArea(app):
    try:
        # Capture the screen area
        screenshot = ImageGrab.grab(bbox=(
            ((1920-app.width)/2)+app.frameX1-50,
            ((1080-app.height)/2)+app.frameY+50,
            (1920-(1920-app.width)/2)+50,
            (1080-(1080-app.height)/2)+50
        ))
        
        # Convert to RGB
        rgbImage = screenshot.convert('RGB')
        
        # Create a new image for processed result
        newImage = Image.new(mode='RGB', size=(app.imageSize, app.imageSize))
        
        # Process each pixel if needed
        for x in range(app.imageSize):
            for y in range(app.imageSize):
                r, g, b = rgbImage.getpixel((x, y))
                # You can process pixels here if needed
                newImage.putpixel((x, y), (r, g, b))
        
        # Save the processed image
        newImage.save('image2Gen.png')
        print("drew imageIn to image2Gen and start reading imageOut")
        
    except Exception as e:
        print(f"Error saving canvas: {e}")

def isInRightCanvas(app, x, y):
    # Check if the point (x,y) is within the RIGHT canvas bounds (where drawing happens)
    return (app.frameX1 <= x <= app.frameX1 + app.imageSize and 
            app.frameY <= y <= app.frameY + app.imageSize)

def drawVolumes(app):
    for i in range(len(app.shapes)):
        shape = app.shapes[i]
        if len(app.colors) != 0:
            color = app.colors[i]
        if shape[0] != shape[1]: # check for clicks in the same place
            firstPoint, secondPoint = shape[0], shape[1]
            width, height = getWidthAndHeight(app, shape)
            # x, y = firstPoint if firstPoint < secondPoint else secondPoint
            x = min(firstPoint[0], secondPoint[0])
            y = min(firstPoint[1], secondPoint[1])
            drawRect(x, y, width, height, fill=color)

def drawBrushStrokes(app, radius):
    if app.isBrushMode:
        drawCircle(app.bx, app.by, radius, fill=None, borderWidth=1, border='black')
    if app.brushLocations != []:
        for location in app.brushLocations:
            x, y = location
            drawCircle(x, y, radius, fill=app.currentColor)

def importImage(app):
   # Create tkinter root window and hide it
   root = tk.Tk()
   root.withdraw()
   
   try:
       # Open file dialog for multiple image selection
       filePaths = filedialog.askopenfilenames(
           title='Select Images',
           filetypes=[
               ('Image files', '*.png *.jpg *.jpeg *.gif *.bmp')
           ]
       )
       
       if filePaths:  # If files were selected
           # Initialize the list if it doesn't exist
           if not hasattr(app, 'importFilePathList'):
               app.importFilePathList = []
           
           # Add new paths to the list
           app.importFilePathList.extend(filePaths)
           app.imageIn = app.importFilePathList[0]  # Set first image as current
           app.showImageIn = True
           print(f'Images imported: {len(filePaths)} files')
           print('Imported paths:', app.importFilePathList)
   except Exception as e:
       print(f'Error importing images: {e}')
   finally:
       root.destroy()

def onMousePress(app, mouseX, mouseY):
    # Check color buttons (top row)
    for i in range(5):
        buttonX = app.buttonStartX + (app.gapX * i)
        buttonY = app.buttonY
        if (buttonX <= mouseX <= buttonX + app.buttonSize and
            buttonY <= mouseY <= buttonY + app.buttonSize):
            app.currentColor = app.buttonColor[i]
            print(f'Color button {app.currentColor} clicked!')
            return
    
    # Check icon buttons (bottom row)
    for i in range(5):
        buttonX = app.buttonStartX + (app.gapX * i)
        buttonY = app.buttonY + app.buttonSize * 2
        if (buttonX <= mouseX <= buttonX + app.buttonSize and
            buttonY <= mouseY <= buttonY + app.buttonSize):
            prevTool = app.currentTool  # Store previous tool
            app.currentTool = app.iconLabel[i]
            
            # Set appropriate states based on selected tool
            if app.currentTool == 'Import':
                importImage(app)
            # Replaced onKeyPress
            if app.currentTool == 'Brush':
                app.isBrushMode = True
                # if prevTool != 'Brush':  # Only clear if switching to brush
                #     app.brushLocations = []
            elif app.currentTool == 'Shape':
                app.isDrawingVolume = True
            elif app.currentTool == 'Erase':
                app.isBrushMode = True
                app.isErasing = True
                if prevTool != 'Erase':  # Only clear if switching to eraser
                    app.brushLocations = []
            elif app.currentTool == 'Reset':
                app.brushLocations = []
                app.currentShape = []
                app.shapes = []
            
            print(f'Switched to {app.currentTool} tool')
            return
        
    if (app.saveButton['x'] <= mouseX <= app.saveButton['x'] + app.saveButton['width'] and
        app.saveButton['y'] <= mouseY <= app.saveButton['y'] + app.saveButton['height']):
        saveCanvasArea(app)
        print("Save button clicked!")
        return

    # Only process drawing if click is within canvas
    if isInRightCanvas(app, mouseX, mouseY):
    ############ Completly same just adding a isInRightCanvas ########################
        app.canvasClicks += 1
        # after 2 clicks in the drawing mode we have created a rectangle
        if app.canvasClicks % 2 == 1:
            if app.isErasing:
                app.colors.append('white')
            else:
                app.colors.append(app.currentColor) if app.currentColor != None else 'black'
            app.currentShape.append((mouseX,mouseY))
        else:
            app.currentShape.append((mouseX,mouseY))
        # after creating the rectangle, clear the current shape
        # and add it to the total shapes list
        if len(app.currentShape) == 2:
            print(f'current shape: {app.currentShape}')
            app.shapes.append(app.currentShape)
            app.currentShape = []

def onMouseDrag(app, mouseX, mouseY):
    if app.isBrushMode and isInRightCanvas(app, mouseX, mouseY):
        # color = 'white' if app.currentTool == 'Erase' else app.currentColor
        app.brushLocations.append((mouseX, mouseY))
        app.bx, app.by = mouseX, mouseY
        print(app.brushLocations)

def onMouseMove(app, mouseX, mouseY):
    app.bx, app.by = mouseX, mouseY

def getWidthAndHeight(app, shape):
    firstPoint, secondPoint = shape[0], shape[1]
    x1, y1 = firstPoint
    x2, y2 = secondPoint
    width = abs(x2 - x1)
    height = abs(y2 - y1)
    return width, height

def onStep(app):
    # Increment step counter
    app.stepCount += 1
    
    # Check if 3 seconds have passed (3 * stepsPerSecond steps)
    if app.stepCount >= (3 * app.stepsPerSecond):
        try:
            if os.path.exists('imageOut.png'):
                app.image2 = 'imageOut.png'
                app.refreshCount += 1
                print(f"Refreshed image {app.refreshCount} times")
        except Exception as e:
            print(f"Error refreshing image: {e}")
        
        # Reset step counter
        app.stepCount = 0

def redrawAll(app):
    # Draw title
    drawLabel('Hackitects', app.width/2, app.frameY/2, size=32, bold=True, fill='black')
    
    # Draw left canvas (drawing area)
    if app.showImageIn and app.imageIn:
        drawImage(app.imageIn, app.frameX1, app.frameY, 
                 width=app.imageSize, height=app.imageSize, opacity=30)
    drawRect(app.frameX1, app.frameY, app.imageSize, app.imageSize, 
            fill=None, border='black', borderWidth=1)
    drawRect(app.frameX1, app.frameY, app.imageSize, app.imageSize, 
            fill=None, border='black', borderWidth=1)
    drawLabel("Draw here or Import Img", app.frameX1 + app.imageSize/2, 
             app.frameY + app.imageSize/2, size=24, bold=True, fill='black')
    
    # Draw right canvas (preview area)
    if app.imageOut is not None:  # Only draw if image exists
        drawImage(app.imageOut, app.frameX2, app.frameY, 
                width=app.imageSize, height=app.imageSize)
    drawRect(app.frameX2, app.frameY, app.imageSize, app.imageSize, 
            fill=None, border='black', borderWidth=1)
    
    # Draw status indicators
    drawLabel(f'Current Tool: {app.currentTool}', 
             app.frameX1 + app.imageSize*1/3, app.frameY - 10)
    drawLabel(f'Current Color: {app.currentColor}', 
             app.frameX1 + app.imageSize*2/3, app.frameY - 10, 
             fill=app.currentColor)
    
    drawRect(app.saveButton['x'], app.saveButton['y'], 
            app.saveButton['width'], app.saveButton['height'],
            fill='lightgrey', border='black')

    drawLabel("Save", 
            app.saveButton['x'] + app.saveButton['width']/2,
            app.saveButton['y'] + app.saveButton['height']/3)  # First line positioned at 1/3
    drawLabel("& Gen", 
            app.saveButton['x'] + app.saveButton['width']/2,
            app.saveButton['y'] +  app.saveButton['height']*2/3)

    
    drawBrushStrokes(app, 5)
    drawVolumes(app)
    
    # Draw color buttons with selection highlight
    for i in range(5):
        isSelected = (app.buttonColor[i] == app.currentColor)
        drawRect(app.buttonStartX+(app.gapX*i), app.buttonY, 
                app.buttonSize, app.buttonSize, 
                borderWidth=3 if isSelected else app.borderW, 
                fill=app.buttonColor[i], 
                border='blue' if isSelected else 'black')
        drawLabel(app.buttonColor[i], 
                 app.buttonStartX + app.buttonSize*1.5 + (app.gapX*i), 
                 app.buttonY + (app.buttonSize/2), 
                 align='left')
    
    # Draw tool buttons with selection highlight
    for i in range(5):
        isSelected = (app.iconLabel[i] == app.currentTool)
        # print(app.iconLabel[i], app.currentTool)
        # Draw icon
        drawImage(app.iconPath[i], 
                 app.buttonStartX+(app.gapX*i), 
                 app.buttonY + app.buttonSize*2, 
                 width=app.buttonSize, height=app.buttonSize,border='blue' if isSelected else None,borderWidth=3 if isSelected else 0)
        drawRect(app.buttonStartX+(app.gapX*i), 
                 app.buttonY + app.buttonSize*2, 
                 app.buttonSize, app.buttonSize,fill = None,border='blue' if isSelected else None,borderWidth=3 if isSelected else 0)
        # Draw label
        drawLabel(app.iconLabel[i], 
                 app.buttonStartX + app.buttonSize*1.5 + (app.gapX*i), 
                 app.buttonY + app.buttonSize*2 + (app.buttonSize/2), 
                 align='left')

def main():
    runApp()

main()