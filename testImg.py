from cmu_graphics import *
from PIL import Image
import os

# Add this function to save the canvas
def saveDrawing(app):
    # Get the pixel data from the drawing area
    pixels = getPixels(app.frameX1, app.frameY, app.imageSize, app.imageSize)
    
    # Create a new image with the same size as the drawing area
    img = Image.new('RGBA', (app.imageSize, app.imageSize))
    
    # Put the pixels into the image
    img.putdata(pixels)
    
    # Save the image
    try:
        # You can change the path and filename as needed
        savePath = 'output_drawing.png'
        img.save(savePath)
        print(f'Drawing saved to {savePath}')
    except Exception as e:
        print(f'Error saving image: {e}')

# Add a key press handler for saving (for example, pressing 's' will save)
def onKeyPress(app, key):
    if key == 's':
        saveDrawing(app)
        print("Drawing saved!")