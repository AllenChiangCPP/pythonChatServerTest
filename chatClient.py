import socket
import threading

# Client configuration
#HOST = '127.0.0.1'
HOST = '192.168.68.134' #for connecting to other computer(server computer's ipv4)
PORT = 55555

#function for receiving message from serber, takes client_socket
def receive_messages(client_socket):
    #while loop to try receiving and decoding utf-8 encrypted message form client_socket,if so print
    while True:
        try:
            # Receive message from the server
            message = client_socket.recv(1024).decode('utf-8')
            print(message)
        #except, if error occurs, connection closed and closed message is printed
        except:
            print("Connection to the server is lost.")
            client_socket.close()
            break

#function for sending message to server, takes client_socket
def send_message(client_socket):
    #while loop, gets user typed message and send to server encoded in utf-8
    while True:
        try:
            # Get input from the user
            message = input("")
            # Send the message to the server
            client_socket.send(message.encode('utf-8'))
        except:
            #except, if error occurs, connection closed and closed message printed
            print("Connection to the server is lost.")
            client_socket.close()
            break

#function for connecting to server
def connect_to_server():
    #create client socket client_socket, AF_INET specifies IPv4, SOCK_STREAM specifies TCP stream sockets
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #connect client socket to server given HOST IP address and PORT number server is listening for incoming connections
    client_socket.connect((HOST, PORT))
    
    #get user inputted username
    username = input("Enter your username: ")
    client_socket.send(username.encode('utf-8'))
    
    print("Connected to the server.")
    
    #start receive_thread for receiving messages using the function receive_messages
    receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
    receive_thread.start()
    
    #Start send_thread for sending messages using function send_message
    send_thread = threading.Thread(target=send_message, args=(client_socket,))
    send_thread.start()

if __name__ == "__main__":
    connect_to_server()