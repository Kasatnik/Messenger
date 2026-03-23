import socket

HOST = "127.0.0.1"
PORT = 4500

client = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
client.connect((HOST, PORT))
while True:
    message_server = input()
    client.send(message_server.encode())
    server_answer = client.recv(1024)
    print(server_answer.decode())


