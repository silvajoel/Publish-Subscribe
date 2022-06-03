import socket, threading  # Libraries import
import sys

host = '127.0.0.1'  # LocalHost
port = int(sys.argv[1])
tags_per_client = {}
FORMAT = "utf8"
TAM = 500

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # socket initialization
server.bind((host, port))  # binding host and port to socket
server.listen()
print("\033[1;32m THE SERVER IS READY \n")

clients = []
nicknames = []


def handle(client, nickname):
    while True:
        try:
            message = client.recv(1024).decode()  # Recieving valid messages from client
            checkTag(client, message)
        except:  # Removing clients
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            nicknames.remove(nickname)
            break


def addTag(client, Tag):

    if (client not in tags_per_client):  # Se o usuário ainda não estiver no dicionário TagsPoClientes
        tags_per_client[client] = [Tag]
        conf = '\033[1;32m > subscribed ' + str(Tag)
        client.send(bytes(conf, "utf8"))
        conf = "\033[1;32m Add \"" + str(Tag) + "\" para cliente " + str(client)
        print(conf)
    else:
        if (Tag not in tags_per_client[client]):  # Caso ele já esteja no dicionário e ainda não possua a tag inserida.
            tags_per_client[client].append(Tag)
            conf = '\033[1;32m > subscribed ' + str(Tag)
            client.send(bytes(conf, "utf8"))
            conf = "\033[1;32m Add \"" + str(Tag) + "\" para cliente " + str(client)
            print(conf)


def delTag(client, Tag):
    if Tag not in tags_per_client[client]:  # Verifica se a Tag que deseja exluir existe.
        client.send(bytes("\033[1;33m not subscribed", "utf8"))
        return

    for i in tags_per_client[client]:  # Remove a Tag de determinado cliente.
        if i == Tag:
            tags_per_client[client].remove(i)
            conf = '\033[0;31m > unsubscribed ' + str(Tag ) + '\033[0;31m'
            client.send(bytes(conf, "utf8"))
            conf = "\033[0;31m Deletando tag \"" + str(Tag) + "\" para cliente " + str(client)
            print(conf)


def remove_duplicate_tags(listTags):  # Remove tags repetidas, para que não sejam armazenadas duplicadas em tags_per_client.
    output = []
    seen = set()
    for value in listTags:
        if value not in seen:
            output.append(value)
            seen.add(value)
    return output


def sendMsg(message, Tags,clientSource):
    Tags = remove_duplicate_tags(Tags)
    for client in tags_per_client:                                                                  # Iterando no dicionário.
        for tagSearch in tags_per_client[client]:                                                   # Iterando em cada cliente do dicionário.
            for Tag in Tags:                                                                        # Caso o cliente seja encontrado, iterar sobre cada tag.
                if tagSearch == Tag and client != clientSource:                                     # Se a tag for igual a tag pesquisada e o cliente for diferente do cliente rementente da mensagem.
                    conf = "Mensagem \"" + str(message) + "\" enviada para cliente " + str(client)
                    print (conf)
                    client.sendall(message.encode('utf-8'))


def splitTags(message):
    MsgList = message.split()
    ListReturn = []
    for i in MsgList:
        if (i[0] == "#"):               # Caso a mesagem contenha alguma hashtag(#), ListReturn recebe as determiandas mensagens de acordo com o caso.
            ListReturn.append(i[1:])
    return ListReturn


def checkTag(client, message):              # Checando a mensagem recebida.

    if message[0] == "+":
        addTag(client, message[1:])         # Caso a mensagem possuir a tag +, como primeiro argumento.
    elif message[0] == "-":
        delTag(client, message[1:])         # Caso a mensagem possuir a tag -, como primeiro argumento.
    else:
        print("\033[1;32m Mensagem recebida: \"" + str(message) + "\"")         # Printa no servidor a mensagem enviada pelo usuário.
        split = splitTags(message)          # Separa a mensagem recebida.
        sendMsg(message, split, client)


def receive():  # accepting multiple clients
    try:
        while True:
            client, address = server.accept()
            print("\033[1;32m Connected with {}".format(str(address)))
            client.send('NICKNAME'.encode(FORMAT))
            nickname = client.recv(TAM).decode(FORMAT)
            nicknames.append(nickname) # Armazerna os nicknames em uma lista
            clients.append(client) # Armazerna os clients(endereços de conexão) em uma lista
            print("\033[1;36m Nickname is {}".format(nickname))
            client.send('\033[1;32m Connected to server!'.encode(FORMAT))
            thread = threading.Thread(target=handle, args=(client, nickname))
            thread.start()
    except KeyboardInterrupt:
        print("caught keyboard interrupt, exiting")
    finally:
        server.close()


receive()
