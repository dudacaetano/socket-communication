import socket
import threading 

HOST = "127.0.0.1"
PORT = 55557


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))


    s.sendall(b"HELLO... \n")
    full_msg = ''
    while True:
        data = s.recv(1024)
        if len(data) <= 0:
            break
        full_msg += data.decode("utf-8")
    

print(full_msg)
#print(data.decode("utf-8"))

#print(f"Received {data}")