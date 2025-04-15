import socket
import threading



# Basic server settings
HOST = '127.0.0.1'  # This is the local machine (localhost)
PORT = 5000         #  change this if busy



# Store all connected clients and their usernames
clients = []
aliases = []


def broadcast(message):
    
    """Send a message to ALL connected clients."""
    for client in clients:
        try:
            client.send(message)
        except:
            print("[SERVER] Failed to send message to a client.")



def handle_client(client_socket):
    
    """Handle messages from one client and send them to everyone."""
    while True:
        try:
            
            # Wait for a message from this client
            message = client_socket.recv(1024)

            # If no message received, its disconnected
            if not message:
                raise ConnectionError

            # Send the message to all other clients
            broadcast(message)


        except:
            
            # If there's an error, remove the client from the list
            if client_socket in clients:
                index = clients.index(client_socket)
                alias = aliases[index]

                clients.pop(index)
                aliases.pop(index)
                client_socket.close()

                broadcast(f"[SERVER] {alias} left the chat.\n".encode('utf-8'))
                print(f"[SERVER] {alias} disconnected.")
            break



def receive_connections(server_socket):
    
    """Accept new clients and start a thread for each one."""
    while True:
        try:
            client_socket, address = server_socket.accept()
            print(f"[SERVER] New connection from {address}")


            # Ask the new client for a username
            client_socket.send("ALIAS".encode('utf-8'))
            alias = client_socket.recv(1024).decode('utf-8').strip()


            # If nothed entered, close the connection
            if not alias:
                client_socket.close()
                continue


            # Save the client info
            aliases.append(alias)
            clients.append(client_socket)


            print(f"[SERVER] {alias} joined the chat.")
            broadcast(f"[SERVER] {alias} has joined the chat!\n".encode('utf-8'))
            client_socket.send("[SERVER] You are now connected!\n".encode('utf-8'))

            # Start a new thread to keep listening to this client
            thread = threading.Thread(target=handle_client, args=(client_socket,))
            thread.start()

        except Exception as e:
            print(f"[SERVER] Error accepting new connection: {e}")



def main():
    
    """This runs when the user types 'startserver' in the terminal."""
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen()

    print(f"[SERVER] Listening on {HOST}:{PORT}...")
    receive_connections(server_socket)
