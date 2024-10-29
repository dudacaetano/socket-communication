import pygame as p

#  utility functions
def directions(x, y, minX=0,minY=0, maxX=7, maxY=7):
    validdirections = []
    if x != minX: validdirections.append((x-1,y))
    if x != minX and y != minY: validdirections.append((x-1, y-1))
    if x != minX and y != maxY: validdirections.append((x-1, y+1))
    
    if x != maxX: validdirections.append((x+1, y))
    if x != maxX and y != minY: validdirections.append((x+1, y-1))
    if x != maxX and y != maxY: validdirections.append((x+1, y+1))
    
    if y != minY: validdirections.append((x, y-1))
    if y != maxY: validdirections.append((x, y+1))
    
    return validdirections
    
def loadImages(path, size):
    """Load an image into the game, and scale the image"""
    img = p.image.load(f"{path}").convert_alpha()
    img = p.transform.scale(img, size)
    return img

def loadSpriteSheet(sheet, row, col, newSize, size):
    """creates an empty surface, loads a portion of the spritesheet onto the surface, then return that surface as img"""
    image = p.Surface((32, 32)).convert_alpha()
    image.blit(sheet, (0, 0), (row * size[0], col * size[1], size[0], size[1]))
    image = p.transform.scale(image, newSize)
    image.set_colorkey('Black')
    return image

