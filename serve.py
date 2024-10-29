
import socket 

# criando o socket do serve 

'''
HOST - addrs to accept conn 
TCP PORT number - each internet service on a computer gets a unique port number (< 1024
reserved for specific services)
'''

HOST = "127.0.0.1"

PORT = 55557

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    # binds this socket to a specific host/port
    s.bind((HOST, PORT))
    s.listen(2)

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
    conn.close()
       
    