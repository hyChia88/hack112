from cmu_graphics import *

def onAppStart(app):
    app.width = 1000
    app.height = 600
    
    # UI Properties===========================================
    # Initialize images
    app.image1 = 'testImg.png'
    app.image2 = 'testImg.png'
    
    # the Icon
    app.iconPath = ['brush.png','shapes.png','eraser.png','import.png','volume.png']
    app.iconLabel = ['Brush', 'Shape', 'Erase', 'Import', 'Volume']
    
    # Button properties
    app.buttonSize = 20
    app.gap = 5
    app.gapX = 150
    app.buttonColor = 100  # Starting X position for buttons
    app.buttonColorName = ['Green','Red','Brown','Black','Grey']
    app.buttonY = 470   # Starting Y position for buttons
    app.borderW = 1
    
    # img size
    app.imageSize = 400
    
    # Store button positions for click detection
    app.colorButtons = []
    app.iconButtons = []
    
    # Initialize color buttons (top row)
    for i in range(5):
        app.colorButtons.append({
            'x': app.buttonColor + (app.gapX * i),
            'y': app.buttonY,
            'type': 'color',
            'color': app.buttonColorName[i]
        })
    
    # Initialize icon buttons (bottom row)
    for i in range(5):
        app.iconButtons.append({
            'x': app.buttonColor + (app.gapX * i),
            'y': app.buttonY + app.buttonSize * 3,
            'type': 'icon',
            'icon': app.iconPath[i],
            'label': app.iconLabel[i]
        })
    
    # Drawing Properties==========================================
    app.shapes = []
    app.currentShape = []
    app.canvasClicks = 0
    app.isDrawingVolume = True
    app.isErasing = False
    app.colors = []
    app.currentColor = 'black'
    app.isBrushMode = False
    app.bx, app.by = None, None
    app.brushLocations = []
    
    # Canvas Properties
    app.canvas2X = 510  # Right canvas X position
    app.canvas2Y = 50   # Right canvas Y position

def isInRightCanvas(app, x, y):
    # Check if the point (x,y) is within the right canvas bounds
    return (app.canvas2X <= x <= app.canvas2X + app.imageSize and 
            app.canvas2Y <= y <= app.canvas2Y + app.imageSize)

def redrawAll(app):
    # Draw white background
    drawRect(0, 0, app.width, app.height, fill='white')
    drawLabel('Hackitects', app.width/2, 30, size=24, bold=True, fill='black')
    
    # Draw first rectangle and image
    drawImage(app.image1, 90, 50, width=app.imageSize, height=app.imageSize)
    drawRect(90, 50, app.imageSize, app.imageSize, fill=None, border='black', borderWidth=1)
    
    # Draw second rectangle and image
    drawImage(app.image2, app.canvas2X, app.canvas2Y, width=app.imageSize, height=app.imageSize)
    drawRect(app.canvas2X, app.canvas2Y, app.imageSize, app.imageSize, fill=None, border='black', borderWidth=1)
    
    # Draw status indicators at the top of right canvas
    drawLabel(f'Current Tool: {"Brush" if app.isBrushMode else "Shape"}', 
             app.canvas2X + app.imageSize//2, app.canvas2Y - 20)
    drawLabel(f'Current Color: {app.currentColor}', 
             app.canvas2X + app.imageSize//2, app.canvas2Y - 40, 
             fill=app.currentColor)
    
    # Draw shapes and brush strokes (only in right canvas)
    drawVolumes(app)
    drawBrushStrokes(app, 5)
    
    # Draw UI buttons
    # Color Buttons
    for i in range(5):
        drawRect(app.buttonColor+(app.gapX*i), app.buttonY, app.buttonSize, app.buttonSize, 
                borderWidth=app.borderW, fill=app.buttonColorName[i], border='black')
        drawLabel(app.buttonColorName[i], 
                 app.buttonColor + app.buttonSize*1.5 + (app.gapX*i), 
                 app.buttonY + (app.buttonSize/2), 
                 align='left')
    
    # Tool Buttons
    for i in range(5):
        drawImage(app.iconPath[i], 
                 app.buttonColor+(app.gapX*i), 
                 app.buttonY + app.buttonSize*3, 
                 width=app.buttonSize, height=app.buttonSize)
        drawLabel(app.iconLabel[i], 
                 app.buttonColor + app.buttonSize*1.5 + (app.gapX*i), 
                 app.buttonY + app.buttonSize*3 + (app.buttonSize/2), 
                 align='left')

def drawVolumes(app):
    for i in range(len(app.shapes)):
        shape = app.shapes[i]
        color = app.colors[i] if len(app.colors) > i else 'black'
        if shape[0] != shape[1]:  # check for clicks in the same place
            firstPoint, secondPoint = shape[0], shape[1]
            width, height = getWidthAndHeight(app, shape)
            x = min(firstPoint[0], secondPoint[0])
            y = min(firstPoint[1], secondPoint[1])
            if isInRightCanvas(app, x, y):
                drawRect(x, y, width, height, fill=color)

def drawBrushStrokes(app, radius):
    if app.isBrushMode and app.bx is not None and app.by is not None:
        if isInRightCanvas(app, app.bx, app.by):
            drawCircle(app.bx, app.by, radius, fill=None, borderWidth=1, border='black')
    
    for location in app.brushLocations:
        x, y = location
        if isInRightCanvas(app, x, y):
            drawCircle(x, y, radius, fill=app.currentColor)

def onMousePress(app, mouseX, mouseY):
    # Check color buttons (top row)
    for i in range(5):
        buttonX = app.buttonColor + (app.gapX * i)
        buttonY = app.buttonY
        if (buttonX <= mouseX <= buttonX + app.buttonSize and
            buttonY <= mouseY <= buttonY + app.buttonSize):
            app.currentColor = app.buttonColorName[i]
            return
    
    # Check icon buttons (bottom row)
    for i in range(5):
        buttonX = app.buttonColor + (app.gapX * i)
        buttonY = app.buttonY + app.buttonSize * 3
        if (buttonX <= mouseX <= buttonX + app.buttonSize and
            buttonY <= mouseY <= buttonY + app.buttonSize):
            if app.iconLabel[i] == 'Brush':
                app.isBrushMode = not app.isBrushMode
            elif app.iconLabel[i] == 'Erase':
                app.isErasing = not app.isErasing
            return

    # Only process drawing if click is within right canvas
    if isInRightCanvas(app, mouseX, mouseY):
        if not app.isBrushMode:  # Shape drawing mode
            app.canvasClicks += 1
            if app.canvasClicks % 2 == 1:
                if app.isErasing:
                    app.colors.append('white')
                else:
                    app.colors.append(app.currentColor)
                app.currentShape.append((mouseX, mouseY))
            else:
                app.currentShape.append((mouseX, mouseY))
                
            if len(app.currentShape) == 2:
                app.shapes.append(app.currentShape)
                app.currentShape = []

def onMouseDrag(app, mouseX, mouseY):
    if app.isBrushMode and isInRightCanvas(app, mouseX, mouseY):
        app.brushLocations.append((mouseX, mouseY))
        app.bx, app.by = mouseX, mouseY

def onMouseMove(app, mouseX, mouseY):
    app.bx, app.by = mouseX, mouseY

def getWidthAndHeight(app, shape):
    firstPoint, secondPoint = shape[0], shape[1]
    x1, y1 = firstPoint
    x2, y2 = secondPoint
    width = abs(x2 - x1)
    height = abs(y2 - y1)
    return width, height

def main():
    runApp(width=1000, height=600)

if __name__ == '__main__':
    main()