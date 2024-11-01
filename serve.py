
import socket 
import threading

# criando o socket do serve 
'''
HOST - addrs to accept conn 
TCP PORT number - each internet service on a computer gets a unique port number (< 1024
reserved for specific services)
'''
HOST = '127.0.0.1'
PORT = 55557

#empty list to store connected clients
clients = []
aliases = []

"""transferring a message to all recipients simultaneously """
def broadcast(data):
     for client in clients:
          client.send(data)
 
def handleClient(client):
     while True:
        try:
             data = client.recv(1024)
             broadcast(data)
        except:
             index = clients.index(client)
             clients.remove(client)
             client.close()
             alias = aliases[index]
             broadcast(f'Connection with{alias} was reset')
             aliases.remove(alias)
             break
# main function to connect all clients
def receive():
     while True: 
         print('Serve is running and trying connect all clients...')   
         client, addr = s.accept()
         print(f"Connected by {str(addr)} has been established")
         client.send('alias?'.encode('utf-8'))
         alias = client.recv(1024)
         aliases.append(alias)
         clients.append(client)
         print(f'The alias of this client is {alias}'.encode('utf-8'))
         broadcast(f'{alias.decode("utf-8")} has connected to th3e chat room'.encode('utf-8'))
         client.send('you are now connected'.encode('utf-8'))
         thread = threading.Thread(target=handleClient, args=(client,))
         thread.start()
              
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    # binds this socket to a specific host/port
    s.bind((HOST, PORT))
    s.listen()
    receive()          
            
    
    
###############################################################
    '''HOST = "127.0.0.1"

    PORT = 55557

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        # binds this socket to a specific host/port
         s.bind((HOST, PORT))
         s.listen(2)
    
         #empty list to store connected clients
         clients = []
         aliases = []        
        
        
    while True:
        conn, addr = s.accept()

        with conn: 
            print(f"Connected by {addr} has been established1")
            conn.send("Welcome to the serve!".encode('utf-8'))
            while True: 
                try:
                    data =  conn.recv(1024).decode('utf-8')
                    if not data: 
                        break
                    print(f"Message from client is: {data}")
                    conn.sendall(data.encode('utf-8'))
                except ConnectionResetError:
                    print(f"Connection with{addr} was reset")
                    break
    conn.close()'''
       
    