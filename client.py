import socket
import threading 

#HOST = '127.0.0.1'
#PORT = 55557

alias = input('Choose an alias>>>')
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
client.connect(('127.0.0.1', 55557))


def client_receive():
    while True:
         try:
            data = client.recv(1024).decode('utf-8')
            if data == "alias?":
                client.send(alias.encode('utf-8'))
            else: 
                print(data)
         except:
            print('ERRO ao receber data!')
            client.close()
            break
def client_send():
    while True:
        try:
            data = f'{alias}: {input("")}'
            client.send(data.encode('utf-8'))
        
        
        except:
            print('ERRO ao enviar dados')
            client.close()
            break

receive_thread =  threading.Thread(target=client_receive)
receive_thread.start()

send_thread = threading.Thread(target=client_send)
send_thread.start()
