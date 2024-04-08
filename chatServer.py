import socket
import threading
import os
from datetime import datetime

# Server configuration
#HOST = '127.0.0.1' #localHost, for computer to computer connection

#for computer to computer connection
#HOST = '0.0.0.0' #unspecifeid address, listens to any available ip address
HOST = '192.168.68.134' #computer's ip

PORT = 55555 #should match
MAX_CLIENTS = 10 #set max number of clients

#hold client connections and their given usernames
clients = []

folder_name = "chatLogs"
current_directory = os.getcwd()
folder_path = os.path.join(current_directory, folder_name)

if not os.path.exists(folder_path):
    os.makedirs(folder_path)

#Function for handling clients, takes in a client's connected socket and their username
def handle_client(client_socket, username):
    broadcast(f"{username} has connected to the server", client_socket)
    with open(chatLog, "a") as f:
                f.write(f"{username} has connected to the server\n")
    #while loop for consta  ntly checking for client messages
    while True:
        #try to receive message using client_socket.receive, and decode utf-8 encoded string, 
        #if there is a message, print in command line, broadcast to other clients, and save to chatlog for the session
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if not message:
                break
            #print message to server's command line
            print(f"[{username}]: {message}")
            
            #Broadcast mesage to other clients
            broadcast(f"[{username}]: {message}", client_socket)
            
            #Save message to current chatlog
            with open(chatLog, "a") as f:
                f.write(f"[{username}]: {message}\n")
        #if an error occurs, connection is closed and client is removed form the list
        except:
            broadcast(f"{username} has disconnected", client_socket)
            print(f"{username} has disconnected")
            with open(chatLog, "a") as f:
                f.write(f"{username} has disconnected\n")
            clients.remove((client_socket, username))
            client_socket.close()
            break

#Function for broadcasting messages to all users, takes in the message and sender_socket
def broadcast(message, sender_socket):
    #go through every client in clients list, try to encode and send message if client is not the sender
    for client, _ in clients:
        if client != sender_socket:
            try:
                #send and encode message using utf-8
                client.send(message.encode('utf-8'))
            except:
                #close connect and remove client from the list of a client has disconnected
                clients.remove((client, _))
                client.close()

#Function for starting the server
def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #create new socket object server, AF_INET specifies IPv4, SOCK_STREAM specifies TCP stream socket
    server.bind((HOST, PORT)) #bind socket to given HOST ip address and PORT port number
    server.listen(MAX_CLIENTS) #sets socket ot listening mode to accept connections
    print(f"Server is listening on {HOST}:{PORT}")
    
    #while loop for accepting connections
    while True:
        #Accept client socket and address, blocks until client connects
        client_socket, client_address = server.accept()
        
        
        #get and decode username fromm the client_scoket using recv
        username = client_socket.recv(1024).decode('utf-8')
        print(f"{username} has connected from ({client_address})")
        #broadcast(f"{username} has connected to the server", client_socket)

        #Add client's socket and username to client list
        clients.append((client_socket, username))
        
        #Start a new threadto handle communicatiosn with the client with the handle_client function
        client_thread = threading.Thread(target=handle_client, args=(client_socket, username))
        client_thread.start()

#Function for saving chat to text file
def save_chat_log(chatLogFile):
    #open given text file as f in write mode
    with open(chatLogFile, "w") as f:
        #goes through usernames in clients, indicates if user has disconnected
        for _, username in clients:
            f.write(f"{username} has disconnected\n")

if __name__ == "__main__":
    #get the date and time, for logging each sessions chatlog
    now = datetime.now()
    dateAndTime = now.strftime("%Y%m%d%H%M%S%f")
    dateAndTime = dateAndTime[:-3]
    #chatLog = f"chat_log_{dateAndTime}.txt"
    chatLog = os.path.join(folder_path, f"chat_log_{dateAndTime}.txt")
    #try staring server, end server wehn programs tops running and save the chat log
    try:
        start_server()
    except KeyboardInterrupt:
        print("\nServer stopped.")
        save_chat_log(chatLog)