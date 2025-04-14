import socket
import threading
import select
import time

# Dicionário para armazenar os clientes conectados e seus nomes de usuário
clientes_conectados = {}

def broadcast(mensagem, remetente_socket=None):
    """Envia a mensagem para todos os clientes, exceto o remetente."""
    for cliente_socket in clientes_conectados.values():
        if cliente_socket != remetente_socket:
            try:
                cliente_socket.send(mensagem.encode('utf-8'))
            except:
                # Remove o cliente se a conexão estiver quebrada
                remover_cliente_por_socket(cliente_socket)

def remover_cliente_por_socket(cliente_socket):
    """Remove o cliente do dicionário baseado no socket."""
    for nome_usuario, sock in list(clientes_conectados.items()):
        if sock == cliente_socket:
            del clientes_conectados[nome_usuario]
            break

def handle_client(client_socket, client_address):
    """Lida com a comunicação com um cliente."""
    print(f"Conexão aceita de {client_address[0]}:{client_address[1]}")

    # Solicita e verifica o nome de usuário
    while True:
        try:
            client_socket.send("Digite seu nome de usuário: ".encode('utf-8'))
            nome_usuario = client_socket.recv(1024).decode('utf-8').strip()
            if not nome_usuario:
                client_socket.send("Nome de usuário não pode ser vazio.\n".encode('utf-8'))
            elif nome_usuario in clientes_conectados:
                client_socket.send("Nome de usuário já em uso. Por favor, escolha outro.\n".encode('utf-8'))
            else:
                clientes_conectados[nome_usuario] = client_socket
                client_socket.send(f"Bem-vindo, {nome_usuario}!\n".encode('utf-8'))
                broadcast(f"{nome_usuario} entrou no chat.", client_socket)
                break
        except:
            client_socket.close()
            return

    def receber_mensagens():
        ultima_mensagem = time.time()  # Marca o tempo da última mensagem recebida
        while True:
            readable, _, _ = select.select([client_socket], [], [], 10)  # Timeout de 10 segundos

            if readable:
                try:
                    mensagem = client_socket.recv(1024).decode('utf-8')
                    if not mensagem:
                        break
                    ultima_mensagem = time.time()  # Atualiza o tempo de última mensagem recebida
                    print(f"{nome_usuario}: {mensagem}")  # Exibe a mensagem no servidor
                    broadcast(f"{nome_usuario}: {mensagem}", client_socket)
                except:
                    break

            # Verifica se o tempo limite de inatividade foi atingido
            if time.time() - ultima_mensagem > 10:
                client_socket.send("Conexão encerrada por inatividade.\n".encode('utf-8'))
                break

        remover_cliente_por_socket(client_socket)
        broadcast(f"{nome_usuario} saiu do chat.", client_socket)
        client_socket.close()

    # Inicia a thread para receber mensagens do cliente
    thread_receber = threading.Thread(target=receber_mensagens)
    thread_receber.start()

def aceitar_conexoes(server):
    """Aceita novas conexões de clientes."""
    while True:
        client_socket, client_address = server.accept()
        client_handler = threading.Thread(target=handle_client, args=(client_socket, client_address))
        client_handler.start()

def enviar_mensagens_servidor():
    """Permite que o servidor envie mensagens para todos os clientes."""
    while True:
        mensagem = input()
        if mensagem.lower() == "sair":
            print("Encerrando o servidor.")
            break
        broadcast(f"Servidor: {mensagem}")

def run_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_ip = "127.0.0.1"
    port = 42000
    server.bind((server_ip, port))
    server.listen()
    print(f"Servidor ouvindo em {server_ip}:{port}")

    # Inicia a thread para aceitar conexões de clientes
    thread_aceitar = threading.Thread(target=aceitar_conexoes, args=(server,))
    thread_aceitar.start()

    # Inicia a função para enviar mensagens do servidor
    enviar_mensagens_servidor()

if __name__ == "__main__":
    run_server()
