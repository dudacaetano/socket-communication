import pygame as p 
import utils.move_logic as move_logic
from gameConstruct import Token 


#Classes

class Grid:
    def __init__(self, rows,columns):
        
        self.y = rows
        self.x = columns
        self.gridLogic = self.regenGrid(rows, columns)
        self.tokens = {}

        
    def regenGrid(self, rows, columns):
        """generate an empty grid for logic use"""
        grid = []
        for y in range(rows):
            line = [0] * columns 
            grid.append(line)
        self.insertToken(grid, -1, 3, 3)
        self.insertToken(grid, 1, 3, 4)
        self.insertToken(grid, -1, 4, 4)
        self.insertToken(grid, 1, 4, 3)

        return grid 
    
    def printGameLogicBoard(self):
        print('  | A | B | C | D | E | F | G | H |')
        for i, row in enumerate(self.gridLogic):
            line = f'{i} |'.ljust(3, " ")
            for item in row:
                line += f"{item}".center(3, " ") + '|'
            print(line)
        print()
        
    def insertToken(self, grid, curplayer, y, x):
        self.tokens[(y, x)] = Token(curplayer, y, x)
        grid[y][x] = self.tokens[(y, x)].player
    
    def findAvailMoves(self, grid, currentPlayer):
         validCells = self.findValidCells(grid, currentPlayer)
         playableCells = []
        
         for cell in validCells:
             x,y = cell
             if cell in playableCells:
                 continue
            
            
             swapTiles = self.swappableTiles(x,y,grid,currentPlayer) 
            
             #if len(swapTiles) > 0 and cell not in playableCells:
             if len(swapTiles) > 0:
                 playableCells.append(cell)
                 
         return playableCells
     
    def findValidCells(self,grid, curPlayer):
        validCellToClick = []
        for gridX, row in enumerate(grid):
            for gridY, col in enumerate(row):
                if grid[gridX][gridY] != 0:
                    continue
                DIRECTIONS = move_logic.directions(gridX, gridY)
                
                for direction in DIRECTIONS:
                    dirX, dirY = direction
                    checkedCell = grid[dirX][dirY]
                    
                    if checkedCell == 0 or checkedCell == curPlayer:
                        continue
                    
                    if (gridX, gridY) in validCellToClick:
                        continue
                    
                    validCellToClick.append((gridX, gridY))
                    
        return validCellToClick
    
     
    def swappableTiles(self, x, y, grid, player):
        surroundCells = move_logic.directions(x, y)
        if len(surroundCells) == 0:
            return[]
        swappableTiles = []
        
        for checkCell in surroundCells:
            checkX, checkY = checkCell
            difX, difY = checkX - x, checkY - y
            currentLine = []
            
            RUN = True
            while RUN:
                #adversario token
                if grid[checkX][checkY] == player * -1: 
                    currentLine.append((checkX, checkY))
                elif grid[checkX][checkY] == player:
                    RUN = False
                    break
                elif grid[checkX][checkY] == 0:
                    currentLine.clear()
                    RUN = False
                    break
                checkX += difX
                checkY += difY
                
                if checkX < 0 or checkX > 7 or checkY < 0 or checkY > 7:
                    currentLine.clear()
                    RUN = False
                    
            if len(currentLine) > 0:
                swappableTiles.extend(currentLine)
                
        return swappableTiles
    
    def calculatePlayerScore(self):
        whiteScore = 0
        blackScore = 0
        emptyScore = 0
        
        for row in self.gridLogic:
            whiteScore += row.score(1)
            blackScore += row.score(-1)
            emptyScore += row.score(0)
        return (whiteScore, blackScore, emptyScore)
    
    def newGame(self):
        self.tokens.clear()
        self.gridLogic = self.regenGrid(self.y, self.x)
        
class DrawGrid:
    def __init__(self, rows,columns, size, main):
        self.GAME = main
        self.y = rows
        self.x = columns
        self.size = size
        self.whitetoken = move_logic.loadImages('socket-communication/assets/WhiteToken.png', size)
        self.blacktoken = move_logic.loadImages('socket-communication/assets/BlackToken.png', size)
        self.transitionWhiteToBlack = [move_logic.loadImages(f'socket_communication/assets/BlackToWhite{i}.png', self.size) for i in range(1, 4)]
        self.transitionBlackToWhite = [move_logic.loadImages(f'/socket_communication/assets/WhiteToBlack{i}.png', self.size) for i in range(1, 4)]
        self.bg = self.loadBackGroundImages()
        
        self.tokens ={}
        
        self.gridBackgraund = self.createBackground()
        
        self.gridLogic = self.regenGrid(self.y, self.x)
    
     
    def regenGrid(self, rows, columns):
        """generate an empty grid for logic use"""
        grid = []
        for y in range(rows):
            line = [0] * columns 
            grid.append(line)
        self.insertToken(grid, -1, 3, 3)
        self.insertToken(grid, 1, 3, 4)
        self.insertToken(grid, -1, 4, 4)
        self.insertToken(grid, 1, 4, 3)

        return grid 
    
    def printGameLogicBoard(self):
        print('  | A | B | C | D | E | F | G | H |')
        for i, row in enumerate(self.gridLogic):
            line = f'{i} |'.ljust(3, " ")
            for item in row:
                line += f"{item}".center(3, " ") + '|'
            print(line)
        print()
        
    def insertToken(self, grid, curplayer, y, x):
        tokenImage = self.blacktoken if curplayer == 1 else self.whitetoken
        self.tokens[(y, x)] = Token(curplayer, y, x, tokenImage, self.GAME)
        grid[y][x] = self.tokens[(y, x)].player
    
    def findAvailMoves(self, grid, currentPlayer):
         validCells = self.findValidCells(grid, currentPlayer)
         playableCells = []
        
         for cell in validCells:
             x,y = cell
             if cell in playableCells:
                 continue
            
            
             swapTiles = self.swappableTiles(x,y,grid,currentPlayer) 
            
             #if len(swapTiles) > 0 and cell not in playableCells:
             if len(swapTiles) > 0:
                 playableCells.append(cell)
                 
         return playableCells
     
    def findValidCells(self,grid, curPlayer):
        validCellToClick = []
        for gridX, row in enumerate(grid):
            for gridY, col in enumerate(row):
                if grid[gridX][gridY] != 0:
                    continue
                DIRECTIONS = move_logic.directions(gridX, gridY)
                
                for direction in DIRECTIONS:
                    dirX, dirY = direction
                    checkedCell = grid[dirX][dirY]
                    
                    if checkedCell == 0 or checkedCell == curPlayer:
                        continue
                    
                    if (gridX, gridY) in validCellToClick:
                        continue
                    
                    validCellToClick.append((gridX, gridY))
                    
        return validCellToClick
    
     
    def swappableTiles(self, x, y, grid, player):
        surroundCells = move_logic.directions(x, y)
        if len(surroundCells) == 0:
            return[]
        swappableTiles = []
        
        for checkCell in surroundCells:
            checkX, checkY = checkCell
            difX, difY = checkX - x, checkY - y
            currentLine = []
            
            RUN = True
            while RUN:
                #adversario token
                if grid[checkX][checkY] == player * -1: 
                    currentLine.append((checkX, checkY))
                elif grid[checkX][checkY] == player:
                    RUN = False
                    break
                elif grid[checkX][checkY] == 0:
                    currentLine.clear()
                    RUN = False
                    break
                checkX += difX
                checkY += difY
                
                if checkX < 0 or checkX > 7 or checkY < 0 or checkY > 7:
                    currentLine.clear()
                    RUN = False
                    
            if len(currentLine) > 0:
                swappableTiles.extend(currentLine)
                
        return swappableTiles
    
    def loadBackGroundImages(self):
        alpha = 'ABCDEFGHI'
        spriteSheet = p.image.load('socket-communication/assets/wood.png').convert_alpha()
        imageDict = {}
        for i in range(3):
            for j in range(7):
                imageDict[alpha[j]+str(i)] = move_logic.loadSpriteSheet(spriteSheet, j, i, (self.size), (32, 32))
        return imageDict
   
    def createBackground(self):
        gridBg = [
            ['C0', 'D0', 'D0', 'D0', 'D0', 'D0', 'D0', 'D0', 'D0', 'E0'],
            ['C1', 'A0', 'B0', 'A0', 'B0', 'A0', 'B0', 'A0', 'B0', 'E1'],
            ['C1', 'B0', 'A0', 'B0', 'A0', 'B0', 'A0', 'B0', 'A0', 'E1'],
            ['C1', 'A0', 'B0', 'A0', 'B0', 'A0', 'B0', 'A0', 'B0', 'E1'],
            ['C1', 'B0', 'A0', 'B0', 'A0', 'B0', 'A0', 'B0', 'A0', 'E1'],
            ['C1', 'A0', 'B0', 'A0', 'B0', 'A0', 'B0', 'A0', 'B0', 'E1'],
            ['C1', 'B0', 'A0', 'B0', 'A0', 'B0', 'A0', 'B0', 'A0', 'E1'],
            ['C1', 'A0', 'B0', 'A0', 'B0', 'A0', 'B0', 'A0', 'B0', 'E1'],
            ['C1', 'B0', 'A0', 'B0', 'A0', 'B0', 'A0', 'B0', 'A0', 'E1'],
            ['C2', 'D2', 'D2', 'D2', 'D2', 'D2', 'D2', 'D2', 'D2', 'E2'],
        ]
        image = p.Surface((960, 960))
        for j, row in enumerate(gridBg):
            for i, img in enumerate(row):
                image.blit(self.bg[img], (i * self.size[0], j * self.size[1]))
        return image
    
    def drawGrid(self, window):
        window.blit(self.gridBackgraund, (0, 0))

        for token in self.tokens.values():
            token.draw(window)
            
        availMoves = self.findAvailMoves(self.gridLogic, self.GAME.currentPlayer)
        #if self.GAME.currentPlayer == 1: //show the validCells just for currentPlayer
        if self.GAME.currentPlayer == self.GAME.currPlayer:
            for move in availMoves:
                p.draw.rect(window, (240,240,240) if self.game.currPlayer == 1 else (50,50,50), (80 + (move[1] * 80) +30,80 +(move[0] *80) +30,20,20))
    
    
    def animateTransitions(self, cell, player):
        if player == 1:
            self.tokens[(cell[0], cell[1])].transition(self.transitionBlackToWhite, self.blacktoken)
        else:
            self.tokens[(cell[0], cell[1])].transition(self.transitionWhiteToBlack, self.whitetoken)
        
    
    def calculatePlayerScore(self):
        whiteScore = 0
        blackScore = 0
        emptyScore = 0
        
        for row in self.gridLogic:
            whiteScore += row.score(1)
            blackScore += row.score(-1)
            emptyScore += row.score(0)
        return (whiteScore, blackScore, emptyScore)
        
    
        
    
        

    
