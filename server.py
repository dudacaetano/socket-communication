
import socket 
import threading
import json

from utils.connectLAN import connectLAN
from utils.notification import NotificationType

from gameConstruct.board import othelloLogic


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


class Server:
    def __init__(self, HOST = '0.0.0.0', PORT=55557):
        self.HOST = HOST
        self.PORT = PORT
        
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((HOST, PORT))
        self.server.listen()
        
        self.clientWhite = None
        self.clientBlack = None 
        
        self.board = othelloLogic(8,8)
        self.gameTurn = -1
        self.endGame = False
        self.whitePoints = 2
        self.blackPoints = 2
        
    def sendMessage(self, message, client):
        if connect := self.clientWhite if client == 1 else self.clientBlack:
            try:
                connect.send(json.dumps(message).encode())
            except (BrokenPipeError, ConnectionResetError):
                print(f"Connection error with client {client}. Removing client")
            
            except Exception as e:
                print(f"Failed to send update to client {client}: {e}")
    
    def sendConfig(self, client):
        message = {
            "type": NotificationType.END_GAME.value,
            "playerTurn": client,
            "board" : self.board.boardLogic,
            "gameTurn": -1}
        self.sendMessage(message, client)
        
    def sendEnfGame(self):
        message = {
            "type": NotificationType.value,
        }
        self.sendMessage(message, 1)
        self.sendMessage(message, -1)
    
    def sendRefresh(self):
        message = {
            "type":NotificationType.value,
            "board": self.board.boardLogic,
            "gameTurn": self.gameTurn
        }
        self.sendMessage(message, self.gameTurn)
    
    #<<<<<<<<<<<<<< FUNCTION OF EXECTIONS >>>>>>>>>>>>>>>>>
    
    def executeMove(self, message):
        x = message.get('x')
        y = message.get('y')
        
        if validCells := self.board.findPlayableMoves(self.board.boardLogic, self.gameTurn):
            if(y, x) in validCells:
                self.board.insertToken(self.board.boardLogic, self.gameTurn, y, x)
                swappableTiles = self.board.fetchSwappableTiles(y,x,self.board.boardLogic,self.gameTurn)
                for tile in swappableTiles:
                    self.board.boardLogic[tile[0]][tile[1]] *= -1
                
                self.gameTurn *= -1
                self.sendRefresh()
                
                if not self.board.findPlayableMoves(self.board.boardLogic, self.gameTurn):
                    self.endGame = True
                    self.sendEnfGame()
                    
    def executeChat(self, message):
        content = message.get('content')
        client = message.get('player')
        
        message = {
            "type": NotificationType.CHAT.value,
            "content": content,
        }
        self.sendMessage(message, client)
    
    def executeGiveup(self, client):
        message = {
            "type": NotificationType.GIVEUP.value
            
        }
        self.sendMessage(message,client*-1)
        
    def executeReset(self):
        self.board.clearBoardLogic()
        self.gameTurn = -1
        self.endGame = False
        self.sendConfig(1)
        self.sendConfig(-1)
        
# <<<<<<<<<<<<< HANDLER FUNCTIONS >>>>>>>>>>>>>>>>>>>>>>>

    def handleMessage(self, connect, message, client): 
        messageType = message.get('type')
        
        if messageType == NotificationType.ACTION.value:
            self.executeMove(message)
        
        elif messageType == NotificationType.CHAT.value:
            self.executeChat(message)
        
        elif messageType == NotificationType.GIVEUP.value:
            self.executeGiveup(client)
            
        elif messageType == NotificationType.RESET.value:
            self.executeReset()         
        
        else:
            print("Unknown message type", message)
            
    def handleClient(self, connect, client):
        self.sendConfig(client)
        
        try:
            while True: 
                data = connect.recv(1024).decode()
                if data:
                    print(f'{client}:{data}')
                    try:
                        message = json.loads(data)
                        self.handleMessage(connect, message, client)
                    except json.JSONDecodeError:
                        print("ERROR decoding the JSON message")
        except(ConnectionResetError, BrokenPipeError):
            print(f"Client {client} disconnected")
            self.disconnClient(client)
        
        finally:
            connect.close()
    
#<<<<<<<<<<<<<<<<<< DISCONNECTED AND CONNECTED CLIENT >>>>>>>>>>>>>>>

    def disconnClient(self, client):
        if client == 1:
            self.clientWhite = None
        
        else:
            self.clientBlack = None
            
        print(f"Client {client} removed. Waiting for new connection")
        
        thread = threading.Thread(target=self.connClient, args=(client,))
        thread.start()
        
    def connClient(self, clientColor):
        connect, addr = self.server.accept()
        print(f"New client connected: {addr} as  {'white' if clientColor == 1 else 'black'}")
        if clientColor == 1:
            self.clientWhite = connect
        else:
            self.clientBlack = connect
        
        thread = threading.Thread(target=self.handleClient, args=(connect, clientColor))
        thread.start()
        
    def run(self):
        print('othelloServer')
        print(f"<<SERVER RUNNING>>('{connectLAN()}', {self.PORT})")
        
        self.connClient(1)
        self.connClient(-1)

if __name__ == "__main__":
    server = Server()
    server.run()
 
                    
         
        
        