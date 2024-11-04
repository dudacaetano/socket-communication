import pygame as p  
from utils.moveLogic import validMoves, loadImages ,getSprites
from gameConstruct.Token import TokenConfig, Token


class othelloLogic:
    def __init__(self, rows, columns):
        self.grid_height = rows
        self.grid_width = columns
        self.tokens = {}
        
        self.boardLogic = self.emptyGrid(rows, columns)
        
    def emptyGrid(self, rows, columns):
        matrix = [[0 for _ in range(columns)] for _ in range(rows)]
        self.insertToken(matrix, 1 , 3 ,3)
        self.insertToken(matrix, -1, 3 , 4)
        self.insertToken(matrix, 1, 4, 4 )
        self.insertToken(matrix, -1, 4 , 3)
        
        return matrix
        
    def displayLogicBoard(self):
        """Prints the current logic board state."""
        print('  | A | B | C | D | E | F | G | H |')
        for i, row in enumerate(self.boardLogic):
            line = f'{i} |'.ljust(3, " ")
            for item in row:
                line += f"{item}".center(3, " ") + '|'
            print(line)
        print()
        
    def insertToken(self, matrix, playerTurn, y, x):
        self.tokens[(y,x)] = TokenConfig(playerTurn,y,x)
        matrix[y][x] = self.tokens[(y,x)].player
    
    def findPlayableMoves(self, matrix, gameTurn):
        validCells = self.findValidCells(matrix, gameTurn)
        playableCells = []
        
        for cell in validCells:
            x, y = cell
            if cell in playableCells:
                continue
            swappableTiles = self.fetchSwappableTiles(x,y, matrix, gameTurn)
            
            if swappableTiles:
                playableCells.append(cell)
                
        return playableCells
    
    def findValidCells(self, matrix, playerTurn):
        
        validCellToClick = []
        
        for gridX, row in enumerate(matrix):
            for gridY, col in enumerate(row):
                if matrix[gridX][gridY] != 0:
                    continue
                DIRECTIONS = validMoves(gridX, gridY)
            
            for direction in DIRECTIONS:
                dirX, dirY = direction
                checkedCell = matrix[dirX][dirY]
                
                if checkedCell == 0 or checkedCell == playerTurn:
                    continue
                
                if (gridX, gridY) in validCellToClick:
                    continue
                
                validCellToClick.append((gridX, gridY))
                
        return validCellToClick
        
    
    def fetchSwappableTiles(self, x, y, matrix, player):
        
        surroundCells = validMoves(x,y)
        
        if not surroundCells:
            return []
        
        swappableTiles = []
        
        for checkCell in surroundCells:
            checkX, checkY = checkCell
            offsetX, offsetY = checkX, checkY
            currentLine = []
            
            
            while True: 
                if matrix[checkX][checkY] == -player:
                    currentLine.append((checkX, checkY))
                elif matrix[checkX][checkY] == player:
                    break
                elif matrix[checkX][checkY] == 0:
                    currentLine.clear()
                    break
                
                checkX += offsetX
                checkY += offsetY
                
                if checkX < 0 or checkX >= self.grid_width or checkY < 0 or checkY >= self.grid_height:
                    currentLine.clear()
                    break
                
            if currentLine:
                swappableTiles.extend(currentLine)
        
        return swappableTiles
    
    def calculatePlayerScore(self):
        whiteScore = 0
        blackScore = 0
        emptyScore = 0
        
        for row in self.boardLogic:
            whiteScore += row.count(1)
            blackScore += row.count(-1)
            emptyScore += row.count(0)
        return (whiteScore, blackScore, emptyScore)
                    
            
    def clearBoardLogic(self):
        self.tokens.clear()
        self.boardLogic = self.emptyGrid(self.grid_height, self.grid_width)


class DrawGrid:
    
    def __init__(self, rows, columns, size, main):
        self.GAME = main
        self.grid_height = rows
        self.grid_width = columns
        self.size = size
        self.whitetoken = loadImages('assets/WhiteToken.png', size)
        self.blacktoken = loadImages('assets/BlackToken.png', size)
        self.transitionWhiteToBlack = [loadImages(f'assets/BlackToWhite{i}.png', self.size) for i in range(1, 4)]
        self.transitionBlackToWhite = [loadImages(f'assets/WhiteToBlack{i}.png', self.size) for i in range(1, 4)]
        
        self.background = self.loadBackGroundImages()
        
        self.tokens ={}
        
        self.gridBackgraundImage = self.createBackground()
        
        self.boardLogic = self.emptyGrid(rows, columns)
        
        
    def emptyGrid(self, rows, columns):
        matrix = [[0 for _ in range(columns)] for _ in range(rows)]
        return matrix
    
    def displayLogicBoard(self):
        """Prints the current logic board state."""
        print('  | A | B | C | D | E | F | G | H |')
        for i, row in enumerate(self.boardLogic):
            line = f'{i} |'.ljust(3, " ")
            for item in row:
                line += f"{item}".center(3, " ") + '|'
            print(line)
        print()
        
    def insertToken(self, matrix, playerTurn, y, x):
        tokenImage = self.whitetoken if playerTurn == 1 else self.blacktoken
        self.tokens[(y,x)] = Token(playerTurn,y,x, tokenImage, self.GAME)
        matrix[y][x] = self.tokens[(y,x)].player
        
    def findPlayableMoves(self, matrix, gameTurn):
        validCells = self.findValidCells(matrix, gameTurn)
        playableCells = []
        
        for cell in validCells:
            x, y = cell
            if cell in playableCells:
                continue
            swappableTiles = self.fetchSwappableTiles(x,y, matrix, gameTurn)
            
            if swappableTiles:
                playableCells.append(cell)
                
        return playableCells
    
    
    def findValidCells(self, matrix, playerTurn):
        
        validCellToClick = []
        
        for gridX, row in enumerate(matrix):
            for gridY, col in enumerate(row):
                if matrix[gridX][gridY] != 0:
                    continue
                DIRECTIONS = validMoves(gridX, gridY)
            
            for direction in DIRECTIONS:
                dirX, dirY = direction
                checkedCell = matrix[dirX][dirY]
                
                if checkedCell == 0 or checkedCell == playerTurn:
                    continue
                
                if (gridX, gridY) in validCellToClick:
                    continue
                
                validCellToClick.append((gridX, gridY))
                
        return validCellToClick
    
    def fetchSwappableTiles(self, x, y, matrix, player):
        
        surroundCells = validMoves(x,y)
        
        if not surroundCells:
            return []
        
        swappableTiles = []
        
        for checkCell in surroundCells:
            checkX, checkY = checkCell
            offsetX, offsetY = checkX, checkY
            currentLine = []
            
            
            while True: 
                if matrix[checkX][checkY] == -player:
                    currentLine.append((checkX, checkY))
                elif matrix[checkX][checkY] == player:
                    break
                elif matrix[checkX][checkY] == 0:
                    currentLine.clear()
                    break
                
                checkX += offsetX
                checkY += offsetY
                
                if checkX < 0 or checkX >= self.grid_width or checkY < 0 or checkY >= self.grid_height:
                    currentLine.clear()
                    break
                
            if currentLine:
                swappableTiles.extend(currentLine)
        
        return swappableTiles
           
    def loadBackGroundImages(self):
        alpha = 'ABCDEFGHI'
        spriteSheet = p.image.load('assets/wood.png').convert_alpha()
        imageDict = {}
        for i in range(3):
            for j in range(7):
                imageDict[alpha[j]+str(i)] = getSprites(spriteSheet, j, i, (self.size), (32, 32))
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
                image.blit(self.background[img], (i * self.size[0], j * self.size[1]))
        return image
    
    def drawGrid(self, window):
        window.blit(self.gridBackgraundImage, (0, 0))

        for token in self.tokens.values():
            token.draw(window)
            
        availMoves = self.findPlayableMoves(self.boardLogic, self.GAME.gameTurn)
        #if self.GAME.currentPlayer == 1: //show the validCells just for currentPlayer
        if self.GAME.gameTurn == self.GAME.playerTurn:
            for move in availMoves:
                p.draw.rect(window, (240,240,240) if self.GAME.playerTurn == 1 else (50,50,50), (80 + (move[1] * 80) +30,80 +(move[0] *80) +30,20,20))
    
    
    def animateTransitions(self, cell, player):
        if player == 1:
            self.tokens[(cell[0], cell[1])].animateTransition(self.transitionBlackToWhite, self.blacktoken)
        else:
            self.tokens[(cell[0], cell[1])].animateTransition(self.transitionWhiteToBlack, self.whitetoken)
        
    
    def calculatePlayerScore(self):
        whiteScore = 0
        blackScore = 0
        emptyScore = 0
        
        for row in self.boardLogic:
            whiteScore += row.count(1)
            blackScore += row.count(-1)
            emptyScore += row.count(0)
        return (whiteScore, blackScore, emptyScore)