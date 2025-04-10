import socket
import threading

def receber_mensagens(client_socket):
    """Recebe mensagens do servidor."""
    while True:
        try:
            mensagem = client_socket.recv(1024).decode('utf-8')
            if not mensagem:
                print("Conexão encerrada pelo servidor.")
                break
            print(mensagem)
        except:
            print("Conexão perdida com o servidor.")
            break

def run_client():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_ip = "127.0.0.1" #aqui preciso informar o IP do servidor (ipconfig)
    server_port = 8000
    client.connect((server_ip, server_port))

    # Recebe e define o nome de usuário
    while True:
        mensagem_servidor = client.recv(1024).decode('utf-8')
        print(mensagem_servidor, end="")
        if "Digite seu nome de usuário:" in mensagem_servidor:
            nome_usuario = input()
            client.send(nome_usuario.encode('utf-8'))
        elif "Bem-vindo" in mensagem_servidor:
            break

    # Inicia a thread para receber mensagens
    thread_receber = threading.Thread(target=receber_mensagens, args=(client,))
    thread_receber.start()

    while True:
        mensagem = input()
        if mensagem.lower() == "sair":
            client.send(f"{nome_usuario} saiu do chat.".encode('utf-8'))
            break
        client.send(mensagem.encode('utf-8'))

    client.close()
    print("Conexão com o servidor encerrada.")

if __name__ == "__main__":
    run_client()
