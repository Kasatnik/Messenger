import socket
import threading

HOST = "0.0.0.0"
PORT = 4500
connections = []
server = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(2)
print(server)


def get_messages(client):
    while True:
        try:
            client_data = client.recv(1024)
            print(client_data)
            if not client_data:
                continue
            for i in connections:
                if i[0] != client:
                    i[0].send(client_data)
        except ConnectionResetError:
            for x in range(len(connections)):
                if client == connections[x][0]:
                    connections.pop(x)
            client.close()
            print("!!!")
            break


while True:
    client, address = server.accept()
    client_name = client.recv(1024)
    for i in connections:
        if i[0] != client:
            i[0].send(f"Подключился {client_name.decode()}".encode())
    connections.append((client, client_name.decode()))
    print(connections)
    thread = threading.Thread(target=get_messages, args=(client,))
    thread.start()
