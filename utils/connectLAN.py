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

#Obtém o IP local da LAN da máquina.
def connectLAN(): 
    
 with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
     try:
         s.connect(('192.168.1.1',1))
         return s.getsockname()[0]
    
     except OSError:
         #retorna '127.0.0.1' se falhar(ex.sem rede)
         return '127.0.0.1'
print("IP local LAN:", connectLAN())