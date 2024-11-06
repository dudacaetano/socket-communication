import socket 
import msgpack as m
import pygame as p  
import threading

from utils.notification import NotificationType
from gameConstruct.board import DrawGrid

class Client:
    def __init__(self, HOST = '0.0.0.0', PORT=55557):
        self.HOST = HOST
        self.PORT = PORT
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        p.init()
        self.gameDisplay = p.display.set_mode((1100, 800), p.DOUBLEBUF)
        self.gameClock = p.time.Clock()
        
        self.playerTurn = 1
        self.gameTurn = -1
        
        self.board = DrawGrid(8, 8, (80, 80), self)
        self.endGame = False
        self.RUN = True
        
        self.INPUT_TEXT = ''
        self.FONT = p.font.SysFont('arial', 18)
        self.chatLog = []
        
        self.whitePoints = 2
        self.whitePointsTxt = 'white'
        self.blackPoints = 2
        self.blackPointsTxt = 'black'
        
    def openConnect(self):
        try:
            self.socket.connect((self.HOST, self.PORT))
            print("Connected to the serve")
        except ConnectionRefusedError:
            print("Failed to connect to the server")
            return
        except Exception as e:
            print(f"An error ocurred while connecting:{e}")
            return
    
    def run(self):
        self.connServer()
        self.openConnect()
        
        threadListen = threading.Thread(target=self.messageListen)
        threadListen.daemon = True
        threadListen.start()
        
    
    def launchRun(self):
        clientHOST, clientPORT = self.socket.getsockname()
        serverHOST, serverPORT = self.socket.getpeername()
        p.display.set_caption(f" OthelloClient {clientHOST}:{clientPORT} connected to server {serverHOST}:{serverPORT}")
        while self.RUN == True: 
            self.input()
            self.draw()
            self.gameClock.tick(60)
            
    #<<<<<<<<<<<<<<<<<<<<<<<<<<< EVENT BUTTON >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    
    def input(self):
        for event in p.event.get():
            if event.type == p.QUIT:
                self.notifyGiveUp()
                self.RUN = False
                
            if event.type == p.TEXTINPUT:
                if len(self.INPUT_TEXT) < 19:
                    self.INPUT_TEXT += event.text
            
            if event.type == p.KEYDOWN:
                if event.key == p.K_BACKSPACE:
                    self.INPUT_TEXT = self.INPUT_TEXT[:-1]
                    
                if event.key == p.K_RETURN and self.INPUT_TEXT != '':
                    self.notifyChatMessage(self.INPUT_TEXT)
                    self.chatLog.append(["s", self.INPUT_TEXT])
                    self.INPUT_TEXT = ''
            
            if event.type == p.MOUSEBUTTONDOWN:
                if event.button == 1:
                    x, y = p.mouse.get_pos()
                    
                    #TODO-logic window endgame
                    if self.endGame:
                        if 800 <= x <= (800+250) and 130 <= y <= (130+30):
                            self.notifyReset()
                    else:
                        if 800 <= x <= (800+250) and 130 <= y <= (130+30):
                            self.notifyGiveUp()
                            self.endGame = True 
                            
                            if self.playerTurn == 1:
                                self.blackPointsTxt += ' YOU ARE THE WINNER!!! '
                                self.whitePointsTxt += ' GAVEUP:( '
                                
                            else:
                                self.whitePointsTxt += ' YOU ARE THE WINNER!!! '
                                self.blackPointsTxt += ' GAVEUP:( '
                                
                        elif self.gameTurn == self.playerTurn:
                            x, y = (x - 80) // 80 , (y - 80) // 80
                            
                            if validCells := self.board.findPlayableMoves(self.board.boardLogic, self.gameTurn):
                                if(y, x) in validCells:
                                    self.board.insertToken(self.board.boardLogic, self.gameTurn, y, x)
                                    swappableTiles = self.board.fetchSwappableTiles(y,x,self.board.boardLogic, self.gameTurn)
                                    for tile in swappableTiles:
                                        self.board.animateTransitions(tile, self.gameTurn)
                                        self.board.boardLogic[tile[0]][tile[1]] *= -1
                                        
                                    
                                    self.notifyAction(x,y)
                                    self.gameTurn *= -1
                                    self.executeScore()
        
    
    def update(self, boardLogic, gameTurn):
        self.board.boardLogic = boardLogic 
        
        #  scroll through the entire boardLogic()
        for y in range(len(boardLogic)):
            for x in range (len(boardLogic[y])):
                if boardLogic[y][x] != 0:
                    player= boardLogic[y][x]
                    
                    self.board.insertToken(self.board.boardLogic, player, y, x)
        
        self.gameTurn = gameTurn
        self.executeScore()
        
    
    def executeScore(self):
        self.whitePoints, self.blackPoints, emptyScore = self.board.calculatePlayerScore()
        
 # <<<<<<<<<<<<<<<<<<<<<<< RENDER FUNCTIONS >>>>>>>>>>>>>>>>>>>>>>>   
    def renderLabel(self, text,x,y, color=(250,250,250)):
        drawImagetxt = self.FONT.render(text, True, color)
        self.gameDisplay.blit(drawImagetxt, (x,y))
        
    def renderBoxChat(self):
        
        p.draw.rect(self.gameDisplay,(20,20,20), [800,200,250,500])
        p.draw.rect(self.gameDisplay,(20,20,20),[800,720,250,30])
        
        self.renderLabel('chat', 830, 175)
        y = 670
        
        for type, content in reversed(self.chatLog[-14:]):
            if type == 'r':
                self.renderLabel(content, 805,y)
            else: self.renderLabel(content, 805,y,(30,120,30))
            y -= 35
        
        self.renderLabel(self.INPUT_TEXT, 805,725)
        
    def renderEndGame(self):
        if self.endGame:
            buttonX, buttonY = 830, 130
            buttonWidth, buttonHeight = 250, 30
            
            resetButtonImage = p.image.load('assets/resetButton.png')
            #resetButtonImage = p.transform.scale(resetButtonImage, (buttonWidth, buttonHeight))
            
            self.gameDisplay.blit(resetButtonImage, (buttonX, buttonY))
        
        '''if self.endGame:
            p.draw.rect(self.gameDisplay,(30,120,30),(800,130,250,30))
            self.renderLabel('RESET', 885, 134, (0, 0, 0))'''
            
    def renderEndGameWindow(self):
        #TODO
        pass
            
    def renderGiveUp(self):
        if not self.endGame:
            
            buttonX, buttonY = 830, 130
            buttonWidth, buttonHeight = 250, 30
            
            resetButtonImage= p.image.load('assets/giveupButton.png')
            resetButtonImage = p.image.load('assets/giveupButton.png')
            
            self.gameDisplay.blit(resetButtonImage, (buttonX, buttonY))
        
        
        '''if not self.endGame:
            p.draw.rect(self.gameDisplay, (139,0,0), (800, 130, 250, 30))
            self.renderLabel('GIVE UP', 885, 134)'''
    
    def draw(self):
        self.gameDisplay.fill((0, 0, 0))
        
        self.board.drawGrid(self.gameDisplay)
        
        self.renderLabel(f'{self.whitePoints}: {self.whitePointsTxt}', 800,60)
        self.renderLabel(f'{self.blackPoints}:{self.blackPointsTxt}', 800,95)
        
        self.renderBoxChat()
        
        self.renderEndGame()
        
        self.renderGiveUp()
        
        p.display.flip()
        

#<<<<<<<<<<<<<<<<<<< LISTEN FUNCTIONS >>>>>>>>>>>>>>>>>>>>
        
    def messageListen(self):
        try:
            while True: 
                # recebe dados em bytes
                data = self.socket.recv(4096)
                if data:
                    print()
                    print(f"Receive message: {data}")
                    
                    try:
                        #desempacota os dados usando msgpack
                        message = m.unpackb(data)
                        self.handleMessage(message)
                    except m.exceptions.ExtraData:
                         print("ERROR decoding the MessagePack message: Extra data encountered")
                    except m.exceptions.UnpackException as e:
                         print(f"ERROR unpacking MessagePack data: {e}")
                         
        except ConnectionResetError:
            print("Connection lost with the server")
        finally:
            self.socket.close()
            
# <<<<<<<<<<<<<<<<< SEND FUNCTIONS >>>>>>>>>>>>>>>>>>>>
    def notifyAction(self, x,y):
        message = {
            "type": NotificationType.ACTION.value,
            "x": x,
            "y": y
        }
        
        packedMessage = m.packb(message)
        self.socket.send(packedMessage)
        
        
    def notifyChatMessage(self,content):
        message ={
            "type": NotificationType.CHAT.value,
            "content": content,
            "player": self.playerTurn *-1
        }
        packedMessage = m.packb(message)
        self.socket.send(packedMessage)
    
    def notifyGiveUp(self):
        self.endGame = True
        message = {
            "type":NotificationType.GIVEUP.value,
        }
        packedMessage = m.packb(message)
        self.socket.send(packedMessage)
        
    def notifyReset(self):
        message = {
            "type": NotificationType.RESET.value,
        }
        packedMessage = m.packb(message)
        self.socket.send(packedMessage)
    
#<<<<<<<<<<<<<<< EXECUTION FUNCTIONS >>>>>>>>>>>>>>>>>>>>>>>
    
    def executeConfig(self, message):
        playerTurn = message.get('playerTurn')
        
        self.endGame = False
        
        self.playerTurn = playerTurn
        self.gameTurn = -1
        self.whitePoints = 2
        self.whitePointsTxt = 'PLAYER-2'
        self.blackPoints = 2
        self.blackPointsTxt = 'PLAYER-1'
        
        self.executeScore()
        
        if self.playerTurn == 1:
            self.whitePointsTxt += '# YOU'
        else: 
            self.blackPointsTxt += '# YOU'
        
        self.board.tokens.clear()
        boardLogic = message.get('board')
        self.update(boardLogic, -1)
        self.endGame = False
        
    
    def executeUpdate(self, message):
        boardLogic = message.get('board')
        gameTurn = message.get('gameTurn')
        self.update(boardLogic, gameTurn)
        
    def executeChat(self, message):
        content = message.get('content')
        self.chatLog.append(['r', content])
        
    def executeEndGame(self):
        self.endGame =True
        
        if self.whitePoints > self.blackPoints:
            self.whitePointsTxt += ' YOU ARE THE WINNER!!! '
            self.blackPointsTxt += ' YOU LOST:( '
        
        elif self.whitePoints < self.blackPoints:
            self.blackPointsTxt += ' YOU ARE THE WINNER!!! '
            self.whitePointsTxt += ' YOU LOST:( '
        
        else:
            self.blackPointsTxt += ' DRAW '
            self.whitePointsTxt += ' DRAW '
        
        self.renderEndGameWindow()
        
    def executeGiveUp(self):
        self.endGame = True
        
        if self.playerTurn == -1:
            self.blackPointsTxt += ' YOU ARE THE WINNER!!! '
            self.whitePointsTxt +=  ' GAVEUP '
        
        else: 
            self.whitePointsTxt += ' WON'
            self.blackPointsTxt += ' GAVEUP'
            
#<<<<<<<<<<<<<<<<<< HANDLER FUNCTIONS >>>>>>>>>>>>>>>>>>
        
    def handleMessage(self, message):
        messageType = message.get('type')
        
        if messageType == NotificationType.REFRESH.value:
            self.executeUpdate(message)
        
        elif messageType == NotificationType.CONFIG.value:
            self.executeConfig(message)
        
        elif messageType == NotificationType.CHAT.value:
            self.executeChat(message)
        
        elif messageType == NotificationType.END_GAME.value:
            self.executeEndGame()
        
        elif messageType == NotificationType.GIVEUP.value:
            self.executeGiveUp()
        
        else:
            print("Unknown message type", message)
    

#<<<<<<<<<<<< call SERVER >>>>>>>>>>>>
    def connServer(self):
        HOST = input('HOST>>>')
        PORT = input('PORT>>>')
        
        self.HOST = HOST
        self.PORT = int(PORT)
        
if __name__ == "__main__":
    client = Client()
    client.run()
    client.launchRun()
        
        
        
        
    
        