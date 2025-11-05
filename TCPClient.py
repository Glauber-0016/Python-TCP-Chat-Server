from socket import *
import threading
import sys


host = '192.168.0.1'
port = 12345

client_socket = socket(AF_INET, SOCK_STREAM)

def receive_messages():
    while True:
        try:
            data = client_socket.recv(1024).decode()
            if not data:
                print("conexão perdida")
                client_socket.close()
                sys.exit()
            
           
            print(f"{data}", end="", flush=True)

        except:
            break

def send_messages():
    username = input("Digite seu nome de usuario: ")
    client_socket.sendall(username.encode())

    while True:
        try:
            message = input("> ")

            if message.lower() in ('/exit', '/quit'):
                client_socket.sendall(message.encode())
                print("encerrando conexão")
                client_socket.close()
                break
            
            if message.startswith('/') and (message.split()[0].lower() in ('/join', '/leave')):
                client_socket.sendall(message.encode())
            
            else:
                client_socket.sendall(message.encode())

        except:
            break


def start_client():

    client_socket.connect((host, port))

    print("conectado ao servidor ")
    threading.Thread(target=receive_messages).start()



if __name__ == "__main__":
    start_client()
