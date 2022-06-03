import socket, threading
import sys

nickname = input("\033[1;36m Choose your nickname: ")
FORMAT = "utf-8"
HOST = sys.argv[1] 
PORT = int(sys.argv[2])


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #socket initialization
client.connect((HOST, PORT)) #connecting client to server

def receive():
    while True: #making valid connection
        try:
            message = client.recv(1024).decode(FORMAT)
            if message == 'NICKNAME':
                client.send(nickname.encode(FORMAT))
            else:
                print(message)
        except: #case on wrong ip/port details
            print("An error occured!")
            client.close()
            break
def write():
    while True: #message layout
        message =  input()
        client.send(message.encode(FORMAT))

receive_thread = threading.Thread(target=receive) #receiving multiple messages
receive_thread.start()
write_thread = threading.Thread(target=write) #sending messages 
write_thread.start()