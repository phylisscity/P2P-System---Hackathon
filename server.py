import socket
import threading


# Server setup (IP & Port)
HOST = '127.0.0.1'  # Local machine (loopback address)
PORT = 5000         # Pick a random open port (above 1024 is safer)


# Keep track of active clients and their chosen names
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
    
    """Listens for messages from ONE client and sends them to everyone."""
    
    while True:
        
        try:
            message = client_socket.recv(1024)  # Try to receive message
            
            if not message:  # Empty message = client disconnected
                raise ConnectionError  

            broadcast(message)  # Send message to all clients
        
        
        except:
            
            # Find the client index (if still in list)
            if client_socket in clients:
                index = clients.index(client_socket)
                alias = aliases[index]  # Get their alias
                
                # Remove them from active users
                clients.pop(index)
                aliases.pop(index)
                
                client_socket.close()  # Close connection
                
                # Notify others that this user left
                broadcast(f"[SERVER] {alias} left the chat.\n".encode('utf-8'))
                print(f"[SERVER] {alias} disconnected.")
            break



def receive_connections():
    
    """Waits for new clients and starts a thread for each one."""
    
    while True:
        
        try:
            client_socket, address = server_socket.accept()  # Accept new client
            print(f"[SERVER] New connection from {address}")

            # Ask the client for their username
            client_socket.send("ALIAS".encode('utf-8'))
            alias = client_socket.recv(1024).decode('utf-8').strip()

            # If alias is empty, reject the connection
            if not alias:
                client_socket.close()
                continue

            # Save client info
            aliases.append(alias)
            clients.append(client_socket)

            print(f"[SERVER] {alias} joined the chat.")
            broadcast(f"[SERVER] {alias} has joined the chat!\n".encode('utf-8'))
            client_socket.send("[SERVER] You are now connected!\n".encode('utf-8'))

            # Start a new thread to listen for messages from this client
            thread = threading.Thread(target=handle_client, args=(client_socket,))
            thread.start()

        except Exception as e:
            print(f"[SERVER] Error accepting new connection: {e}")




# Set up the server
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen()

print(f"[SERVER] Listening on {HOST}:{PORT}...")

receive_connections()  # Start accepting clients
