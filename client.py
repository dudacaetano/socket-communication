import socket
import threading 

#HOST = '127.0.0.1'
#PORT = 55557


class OthelloClient:
    def __init__(self, HOST = '0.0.0.0', PORT=55557):
        self.HOST = HOST
        self.PORT = PORT
        
    def setupClient(self):
        try:
            c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            c.connect((self.HOST, self.PORT))
        except ConnectionRefusedError:
            print("<<<NOT CONNECT TO THE OTHELLO-SERVE>>>")
            return
    
