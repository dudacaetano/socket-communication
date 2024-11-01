import socket
import threading 

HOST = '127.0.0.1'
PORT = 55557

alias = input('Choose an alias:')


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as c:
    c.connect((HOST, PORT))


def client_receive():
    while True:
         try:
            data = c.recv(1024).decode('utf-8')
            if data == "alias?":
                c.send(alias.encode('utf-8'))
            else: 
                print(data)
         except:
            print('ERRO!')
            c.close()
            break
def client_send():
    while True:
        data = f'{alias}: {input("")}'
        c.send(data.encode('utf-8'))

receive_thread =  threading.Thread(target=client_receive)
receive_thread.start()

send_thread = threading.Thread(target=client_send)
send_thread.start()
