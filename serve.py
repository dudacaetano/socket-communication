
import socket 
import threading
import json

from utils.connectLAN import connectLAN
from gameConstruct.board import gridLogic
from utils.notification import NotificationType


# criando o socket do serve 
'''
HOST - addrs to accept conn 
TCP PORT number - each internet service on a computer gets a unique port number (< 1024
reserved for specific services)
'''
#HOST = "192.168.0.246"
#PORT = 55557

# create the socket
# AF_INET == ipv4
# SOCK_STREAM == TCP


class OthelloServe: 
    def __init__(self, HOST='0.0.0.0', PORT=55557):
        self.HOST = HOST
        self.PORT = PORT
        
        self.clientWhite = None
        self.clientBlack = None
        
        self.serve = self.setupServe()
    
        self.whitePoints = 2
        self.blackPoints = 2
        
        self.grid = gridLogic(8,8)
        self.currentPlayer = -1
        self.endGame = False
        
    def setupServe(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((self.HOST,self.PORT))
        s.listen(2)
        
        print(f"SERVE running at {self.HOST}:{self.PORT}")
        return s
    

#enviando e recebendo menssagem     

    def sendText(self, client, text):
         connect = self.whitePoints if client == 1 else self.blackPoints
         if connect:
             try:
                 connect.send(json.dumps(text).encode())
             except(BrokenPipeError, ConnectionResetError):
                 print(f"Connection error with client{client}. Disconnecting")
                 
    def sendRun(self, client):
        text = {
            "type": NotificationType.INITIALIZE.value,
            "currPlayer":client,
            "grid":self.grid.gridLogic,
            "currentPlayer":-1
        }
        self.sendText(client, text)
        
    def sendEndGame(self):
        text = {"type": NotificationType.END_GAME.value,
        }
        self.sendText(text,1)
        self.sendText(text,-1)
        
    def sendUpdate(self):
        text = {
            "type": NotificationType.REFRESH.value,
            "grid":self.grid.gridLogic,
            "currentPlayer": self.currentPlayer
        }
        self.sendText(self.currentPlayer, text)
        
        
    def handlerAction(self, text):
        x = text.get('x')
        y = text.get('y')
        if validCells := self.grid.findAvailMoves(self.grid.gridLogic, self.currentPlayer):
            if (y, x) in validCells:
                self.grid.insertToken(self.grid.gridLogic, self.currentPlayer, y, x)
                swapTiles = self.grid.swappableTiles(y, x, self.grid.gridLogic, self.currentPlayer)
                for tile in swapTiles:
                    self.grid.gridLogic[tile[0]][tile[1]] *= -1
                self.currentPlayer *= -1
                self.sendUpdate()

                if not self.grid.findAvailMoves(self.grid.gridLogic, self.currentPlayer):
                    self.endGame = True
                    self.sendEndGame()
        
        
    def handlerMessage(self,client,text):
        content = text.get('content')
        client = text.get('player')
        text = {
        "type": NotificationType.MESSAGE.value,
        "content": content, 
        }
        self.sendText(text, client)
        
    def handlerGiveup(self,client):
        text = {
            "type": NotificationType.GIVEUP.value
        }
        self.sendText(text, client*-1)
        
    def handlerReset(self):
        self.grid.newGame()
        self.currentPlayer = -1
        self.endGame = False
        self.sendRun(1)
        self.sendRun(-1)
        
    
    def handleText(self, client, text):
        textType = text.get('type')
        
        if textType == NotificationType.ACTION.value:
            self.handlerAction(text)
        elif textType == NotificationType.MESSAGE.value:
            self.handlerMessage(client,text)
        elif textType == NotificationType.GIVEUP.value:
            self.handlerGiveup(client)
        elif textType == NotificationType.RESET.value:
            self.handlerReset()
        else:
            print("Unknown message type:", text)
    
    
    
    def handleClient(self, connect, client):
        self.sendRun(client)
        try:
            while True:  
                data = connect.recv(1024).decode()
                if data:
                    text = json.loads(data)
                    self.handleClient(client, text)
        except ConnectionResetError:
            print(f"Client {client} disconnected")
        finally:
            connect.close()
            
    def disconnectClient(self, client):
        
        if client == 1:
            self.clientWhite = None
        else:
            self.clientBlack = None 
        
        print(f"Client {client} removed. Waiting for new connection")
        
        thread = threading.Thread(target=self.waitNewClients, args=(client,))
        thread.start()
    
    def waitNewClients(self, client_color):
        connect, addr = self.s.accept()
        print(f"New client connected: {addr} as {'white' if client_color == 1 else 'black' }")
        if client_color == 1:
            self.clientWhite = connect
        else:
            self.clientBlack = connect
        
        thread = threading.Thread(target=self.handleClient, args=(connect, client_color))
        thread.start()
              
            
   
    def run(self):
        print('Othello Serve')
        print(f" SERVE RUNNING>>> ('{connectLAN()}', {self.PORT})")
        
        self.waitNewClients(1)
        self.waitNewClients(-1)   
        
if __name__ == "__main__":
    OthelloServe().run()    
        
        
 
                    
         
        
        