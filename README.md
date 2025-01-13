<h1 align="center">
⚪<br>Othello-Reversi Game
</h1>

<img align="center" src="\assets\tabuleiro.jpeg">

## 📚 Resumo
> Othello é um jogo de estratégia para dois jogadores (Pretas e Brancas), jogado num tabuleiro 8x8. A partida começa com quatro peças colocadas no centro do tabuleiro com mostrado abaixo. Pretas fazem a primeira jogada. Os jogadores alternam a vez. Se um jogador não tem jogada válida, passa a vez para o adversário.O jogador com mais peças no tabuleiro ao final do jogo vence. Se ambos tiverem a mesma quantidade de peças, há empate.

# Recursos Principais:
>Este projeto implementa um sistema de comunicação baseado na arquitetura cliente-servidor utilizando sockets. Ele demonstra como dispositivos podem trocar informações em rede de forma eficiente usando o protocolo TCP/IP


**Gráficos Simples:** O jogo possui gráficos 2D, com uma interface de usuário limpa e fácil de entender.

Movimentação das peças: As peças podem se mover horizontalmente e verticalmente, apenas pulando outras peças, jogando em espaços vazios.

Chat: É possível se comunicar com o adversário durante toda a partida.

Desistência: Também é possível desistir no meio da partida

Opção de Reinício: Após o término do jogo, os jogadores têm a opção de reiniciar imediatamente.

## Clone Repositório:
```bash
git clone https:https://github.com/dudacaetano/socket-communication
cd socket-communication
```

## Config ambiente virtual

```bash
python -m venv .venv
source .venv/bin/activate
```

## Instalando Dependencias

```bash
pip install -r requirements.txt
```

## Iniciando Servidor

```bash
python server.py
```

output:

```bash
pygame-ce 2.5.1 (SDL 2.30.6, Python 3.9.6)
Enter the server port:55557
Server Running: ('192.168.x.x', 55557)
```

##  Clientes

Para jogar, você precisa iniciar dois clientes. Os clientes podem ser executados em qualquer máquina da rede local. Ao executar o cliente, você precisará inserir o host (endereço IP) do servidor e o número da porta.

### Executando Clientes:

```bash
python client.py
```

Retorno:

```bash
pygame-ce 2.5.1 (SDL 2.30.6, Python 3.9.6)
Enter the server IP to connect: 192.168.x.x
Enter the server port to connect: 55557
Connected.
```
