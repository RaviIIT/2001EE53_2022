#imports
import socket
from tkinter import messagebox 
import threading

# hashtable for username and passwords
username_hashtable = {}

class ChatServer:
    # list of clients
    clients_list = []
    
    # last message for communication b/w server and client
    last_received_message = ""

    def __init__(self):
        self.server_socket = None
        self.create_listening_server()
    
    #listen for incoming connection
    def create_listening_server(self):
    
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #create a socket using TCP port and ipv4
        local_ip = '127.0.0.1'
        local_port = 10319
        # this will allow you to immediately restart a TCP server
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # this makes the server listen to requests coming from other computers on the network
        self.server_socket.bind((local_ip, local_port))
        print("Listening for incoming messages..")
        self.server_socket.listen(20) #listen for incomming connections / max 5 clients
        self.receive_messages_in_a_new_thread()
        
    #function to receive new msgs
    def receive_messages(self, s):
        while True:
            incoming_buffer = s.recv(256) #initialize the buffer
            # print(incoming_buffer)
            if not incoming_buffer:
                break
            self.last_received_message = incoming_buffer.decode('utf-8')
            
            # reset password encoded with this string pattern
            if '--reset--' in str(self.last_received_message):
                new_usr_name = str(self.last_received_message).split('--reset--')[0]
                new_usr_pass = str(self.last_received_message).split('--reset--')[1]
                username_hashtable[new_usr_name] = new_usr_pass
            elif '=' in str(self.last_received_message):                
                usr_name = str(self.last_received_message).split('=')[0]
                usr_pass = str(self.last_received_message).split('=')[1]
                
                self.last_received_message = str(self.last_received_message).split('=')[0]
                # new user
                if usr_name not in username_hashtable:
                    username_hashtable[usr_name] = usr_pass
                    self.broadcast_to_all_clients(s)  # send to all clients    
                else:
                    if str(username_hashtable[usr_name]) != str(usr_pass):          #incorrect password
                        self.last_received_message = 'error'
                        self.broadcast_to_all_clients(s)
                    else:
                        self.broadcast_to_all_clients(s)  # send to all clients   
            else:
                self.broadcast_to_all_clients(s)  # send to all clients   

        s.close()
    
    #broadcast the message to all clients 
    def broadcast_to_all_clients(self, senders_socket):
        for client in self.clients_list:
            socket, (ip, port) = client
            if socket is not senders_socket:
                socket.sendall(self.last_received_message.encode('utf-8'))

    def receive_messages_in_a_new_thread(self):
        while True:
            client = s, (ip, port) = self.server_socket.accept()
            # added client
            self.add_to_clients_list(client)
            print('Connected to ', ip, ':', str(port))
            # receive messages called
            t = threading.Thread(target=self.receive_messages, args=(s,))
            t.start()
            
    #add a new client 
    def add_to_clients_list(self, client):
        if client not in self.clients_list:
            self.clients_list.append(client)
        print(len(self.clients_list))


if __name__ == "__main__":
    ChatServer()