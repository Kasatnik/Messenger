import socket
import threading
from datetime import datetime
from zoneinfo import ZoneInfo


HOST = "0.0.0.0"
PORT = 4500
connections = []
server = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(2)
print(server)

history = []


# def broadcast_clients():
#    clients_list = [name for sock, name in connections]
#    message = "CLIENTS_LIST:" + ",".join(clients_list)
#    for sock, _ in connections:
#        try:
#            sock.send(message.encode())
#        except:
#            pass


def get_messages(client):
    while True:
        moscow_time = datetime.now(ZoneInfo("Europe/Moscow"))
        try:
            time = moscow_time.strftime("%H:%M:%S")
            client_data = client.recv(1024)
            print(client_data)
            history.append(client_data.decode() + "\n")
            if not client_data:
                continue
            for i in connections:
                i[0].send(time.encode())
                if i[0] != client:
                    i[0].send(client_data)
        except ConnectionResetError:
            for x in range(len(connections)):
                if client == connections[x][0]:
                    connections.pop(x)
            client.close()
            # broadcast_clients()
            print("!!!")
            break


while True:
    client, address = server.accept()
    client_name = client.recv(1024)
    for p in history:
        client.send(p.encode())
    for i in connections:
        if i[0] != client:
            i[0].send(f"Подключился {client_name.decode()}".encode())

    connections.append((client, client_name.decode()))
    # broadcast_clients()
    thread = threading.Thread(target=get_messages, args=(client,))
    thread.start()


    """1. Новые сообщения появляются сверху, давай сделаем наоборот, чтобы они были всё ниже и ниже 

2. К сообщениям добавить время отправки. Важно: пусть сервер занимается временем, НЕ клиент. 

Вкратце: у нас с тобой может быть разное время (например, я в Америке, а ты в России, у нас разница 7 часов примерно). Пусть сервер привязывается к европейскому часовому поясу +0. В идеале конечно сделать так, чтобы я в своем клиенте видел время для своего часового пояса, а ты для своего, но это уже по желанию)

3. В клиенте просто рядом где-то отображать список подключенных клиентов (айпишники + имена). Если кто-то подключился - добавляем и видим тех, кто сейчас "в сети". Если кто-то вышел - удаляем 

4. Ситуация: мы с тобой общаемся в мессенджере уже полчаса, но подключается Дима и не видит прошлую переписку. Было бы круто иметь историю чата, которая сразу при коннекте будет отображаться в клиенте, чтобы все видели предыдущие сообщения 

5. Видеть, что человек "Печатает...". 

Логика такая: следим а ткинтере, что пользователь что-то набирает в инпуте и отправляем это сразу на сервер. Говорим серверу, что я (Рома) пишу в данную секунду и сервер уже передает Паше информацию, где будет отображаться "Roman is typing..."

6. Попробовать разобраться самому, как с клиента отправить какой-либо файл на сервер, чтобы сервер дальше разослал всем клиентам, например, какую-то картинку. Тут, конечно же, использовать гпт или гугл, но тщательно разбирать каждую строчку :))"""
