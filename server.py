import threading
import socket

host = '127.0.0.1'
port = 59000
#server object
server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)#TCP

#blind server to the host and port (here one argument and two given)
#server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((host,port))
#when client send message to other one we need to send to server first and server listen
server.listen()
clients = []
aliases=[]

#send message from server to all connected clients
def broadcast(message):
    for client in clients:
        client.send(message)

#handle clients connection
def handle_client(client):
    while True:
        try:
            message = client.recv(1024) # reads incoming messages from the client 
            broadcast(message) # Manage received messages
        except:
            index=clients.index(client)
            clients.remove(client)
            client.close()
            alias = aliases[index]
            broadcast(f'{alias} has left the chat room!'.encode('utf-8'))
            aliases.remove(alias)
            break

#main function to receive the clients conn
def receive():
    while True:
        print('Server is running and listening ...')
        clinet,address=server.accept() # waits for incoming connections 
        print(f'connection is established with {str(address)}')
        clinet.send('alias?'.encode('utf-8')) # للتشفير 
        alias = clinet.recv(1024)
        aliases.append(alias)
        clients.append(clinet)
        print(f'The alias of this client is {alias}'.encode('utf-8'))
        broadcast(f'{alias} has connected t othe caht room'.encode('utf-8'))
        clinet.send('you are now connected!'.encode('utf-8'))
        thread = threading.Thread(target=handle_client,args=(clinet,))
        thread.start()
if __name__ == "__main__":
    receive()