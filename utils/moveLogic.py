import pygame as p 

#utility functions 


def validMoves(x, y, minX = 0, minY=0, maxX=7, maxY=7):
    """
    Calculate valid moves for a piece on a board.

    Args:
        x (int): Current x-coordinate of the piece.
        y (int): Current y-coordinate of the piece.
        minX (int): Minimum x boundary.
        minY (int): Minimum y boundary.
        maxX (int): Maximum x boundary.
        maxY (int): Maximum y boundary.

    Returns:
        list: A list of tuples representing valid move coordinates.
    """
    
    moves = []
    
    if x > minX:
        moves.append((x - 1, y))
        if y > minY:
            moves.append((x -1, y - 1))
        if y < maxY:
            moves.append((x - 1, y + 1))
    
    if x < maxX:
        moves.append(( x + 1, y))
        
        if y > minY:
            moves.append((x + 1, y - 1))
        if y < maxY:
            moves.append((x + 1, y + 1))
            
    if y > minY:
        moves.append((x, y - 1))
        
    if y < maxY:
        moves.append((x , y + 1 ))
        
    return moves 

def loadImages(path,size):
    image = p.image.load(path).convert_alpha()
    return p.transform.scale(image, size)

def getSprites(sheet, row, columns, size, spriteSize):
    
    sprite = p.Surface((32, 32)).convert_alpha()
    sprite.blit(sheet, (0, 0), (row * spriteSize[0], columns * spriteSize[1], spriteSize[0], spriteSize[1]))
    sprite = p.transform.scale(sprite, size)
    sprite.set_colorkey('Black')
    return sprite
