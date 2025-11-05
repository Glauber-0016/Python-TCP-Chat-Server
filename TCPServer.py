from socket import *
import threading
import sys

client = {}   
rooms = {}   
lock = threading.Lock()

host = '192.168.0.2'
port = 123456


def broadcast(room_name, message, sender_socket=None):
    with lock:
        if room_name in rooms:
            for client_socket in rooms[room_name]:
                if client_socket != sender_socket:
                    try:
                        client_socket.sendall(message.encode())
                    except:
                        pass

def handle_client(conn, addr):
    try:
        username = conn.recv(1024).decode().strip()
    except:
        conn.close()
        return

    with lock:
        client[conn] = {"username": username, "room": None}
        print(f"Novo cliente {username} ({addr}) conectado.")
    
    conn.sendall("Use /join #nome_sala".encode())


    while True:
        try:
            data = conn.recv(1024).decode().strip()
            if not data:
                break 
            
            if data.startswith('/'):
                parts = data.split()
                command = parts[0].lower()
                
                if command == '/exit' or command == '/quit':
                    break 
                
                elif command == '/join' and len(parts) == 2:
                    room_name = parts[1].lower()
                    join_room(conn, username, room_name)
                    
                else:
                    conn.sendall("comando invalido.".encode())
            
            else:
                current_room = client[conn]["room"]
                if current_room:
                    full_message = f"[{current_room}] <{username}>: {data}"
                    broadcast(current_room, full_message, conn)
                else:
                    conn.sendall("não".encode())

        except:
            break 


    disconnect_client(conn, addr, username)


def join_room(client_socket, username, room_name):
    with lock:
        old_room = client[client_socket]["room"]
        if old_room and client_socket in rooms.get(old_room, []):
            rooms[old_room].remove(client_socket)
            broadcast(old_room, f"{username} deixou a sala.", client_socket)
            if not rooms[old_room]:
                del rooms[old_room]
        
        if room_name not in rooms:
            rooms[room_name] = [] 
            
        rooms[room_name].append(client_socket)
        client[client_socket]["room"] = room_name
        
        client_socket.sendall(f" entrou na sala {room_name}.".encode())
        broadcast(room_name, f"{username} entrou na sala.", client_socket)


def disconnect_client(conn, addr, username):
    with lock:
        current_room = client[conn]["room"]
        if current_room and conn in rooms.get(current_room, []):
            rooms[current_room].remove(conn)
            broadcast(current_room, f"{username} desconectou", conn)
            if not rooms[current_room]:
                del rooms[current_room]

        if conn in client:
            del client[conn]
        
        print(f"conexão com {username} ({addr}) acabou")
        conn.close()


def start_server():
    serversocket = socket(AF_INET, SOCK_STREAM)
    serversocket.bind(("", port))
    serversocket.listen(5)
    print(f"servidor ouvindo em {host}:{port}")

    while True:
        conn, addr = serversocket.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()


if __name__ == "__main__":
    start_server()
