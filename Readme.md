# Projeto de Chat em Python

Este projeto implementa uma aplicação de chat simples utilizando sockets em Python, permitindo a comunicação em tempo real entre múltiplos clientes conectados a um servidor central.

A aplicação consiste em um servidor que gerencia conexões de múltiplos clientes, permitindo que eles troquem mensagens em tempo real. O servidor retransmite as mensagens recebidas para todos os clientes conectados, criando assim uma sala de bate-papo coletiva.

## Funcionalidades

- **Servidor:**
  - Aceita conexões de múltiplos clientes simultaneamente.
  - Recebe mensagens de um cliente e as retransmite para todos os outros clientes conectados.
  - Notifica todos os clientes quando um novo usuário entra ou sai do chat.

- **Cliente:**
  - Conecta-se ao servidor especificado.
  - Envia mensagens para o servidor, que as distribui aos demais clientes.
  - Exibe mensagens recebidas de outros clientes em tempo real.

## Como Usar
- **Configure o servidor para aceitar conexões externas:**
  - No arquivo server.py, certifique-se de que o servidor está configurado para ouvir em todas as interfaces de rede, definindo o IP do servidor como '0.0.0.0':

```bash
server_ip = '0.0.0.0'
server_port = 8000
```
- Isso permitirá que o servidor aceite conexões de outros dispositivos na mesma rede.

- **Configure o cliente para conectar-se ao servidor:**
   - No arquivo client.py, atualize as variáveis server_ip e server_port para corresponderem ao endereço IP do servidor e à porta em que ele está ouvindo:
```bash
server_ip = '192.168.1.100'  # Substitua pelo IP do servidor
server_port = 8000
```
