import socket

#SOCK_DGRAM:cria um socket de datagrama (usando o protocolo UDP), que é sem conexão. 
#Isso significa que não há estabelecimento de conexão completo entre cliente e servidor 
#como em SOCK_STREAM (protocolo TCP).

'''
Para obter o IP local, não precisamos de uma comunicação de dados verdadeira.
Precisamos apenas simular uma tentativa de conexão para que o sistema escolha a 
interface de rede e retorne o IP local.
Como SOCK_DGRAM não exige conexão contínua,
ele torna a operação mais rápida e simples.
'''
def connectLAN():
    connectSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    connectSocket.settimeout(0)
    try:
        # Attempt to connect to any IP address (it doesn't matter which)
        connectSocket.connect(('10.254.254.254', 1))
        ipLocal = connectSocket.getsockname()[0]  # Returns the local IP
    except Exception:
        ipLocal = '127.0.0.1'  # Fallback to localhost if it fails
    finally:
        connectSocket.close()
    return ipLocal