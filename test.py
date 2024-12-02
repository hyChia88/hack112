from cmu_graphics import *

def onAppStart(app):
    app.shapes = []
    app.currentShape = []
    app.canvasClicks = 0
    app.isDrawingVolume = True
    app.isErasing = False
    app.colors = []
    app.isDrawingGreen = False
    app.isDrawingBrown = False
    app.isDrawingRed = False
    app.isDrawingGrey = False
    app.colorSelector = {'r':'red', 'g':'green', 'b':'brown', 'm':'grey'}
    app.currentColor = 'black'
    app.stepsPerSecond = 100
    app.isBrushMode = False
    app.bx, app.by = None, None
    app.brushLocations = []

def redrawAll(app):
    brushText = 'brush: [x]' if app.isBrushMode else 'brush: [ ]'
    drawLabel(f'Test!', app.width/2, app.height/2-180)
    drawLabel(f'current color = {app.currentColor}', app.width/2, app.height/2-140, fill=app.currentColor)
    drawLabel(brushText, app.width/2, app.height/2-120, fill=app.currentColor)
    # color = 'black' if app.isDrawingVolume else 'white'
    drawVolumes(app)
    drawBrushStrokes(app, 5)
    text = 'we are filling' if app.isDrawingVolume else 'we are erasing'
    drawLabel(text, app.width/2, app.height/2-160)

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

def onMousePress(app, mx, my):
    app.canvasClicks += 1
    # after 2 clicks in the drawing mode we have created a rectangle
    if app.canvasClicks % 2 == 1:
        if app.isErasing:
            app.colors.append('white')
        else:
            app.colors.append(app.currentColor) if app.currentColor != None else 'black'
        app.currentShape.append((mx,my))
    else:
        app.currentShape.append((mx,my))
    # after creating the rectangle, clear the current shape
    # and add it to the total shapes list
    if len(app.currentShape) == 2:
        print(f'current shape: {app.currentShape}')
        app.shapes.append(app.currentShape)
        app.currentShape = []

def onStep(app):
    pass

def onKeyPress(app, key):
    # eraser mode
    if key == 'e':
        app.isErasing = not app.isErasing
    # all other modes
    elif key in 'brgm':
        app.currentColor = app.colorSelector[key]
    elif key == 'p':
        app.isDrawingVolume = not app.isDrawingVolume
        app.isBrushMode = not app.isBrushMode

def onMouseDrag(app, mx, my):
    if app.isBrushMode:
        app.brushLocations.append((mx,my))
        app.bx, app.by = mx, my
    print(app.brushLocations)

def onMouseMove(app, mx, my):
    app.bx, app.by = mx, my

def getWidthAndHeight(app, shape):
    firstPoint, secondPoint = shape[0], shape[1]
    start = firstPoint if firstPoint < secondPoint else secondPoint
    end = secondPoint if firstPoint < secondPoint else firstPoint
    x1, y1 = start
    x2, y2 = end
    width = abs(max(x2, x1) - min(x1, x2))
    height = abs(min(y2, y1) - max(y1, y2))
    return width, height

def main():
    runApp()

main()