import socket
import threading



# Basic server settings
HOST = '127.0.0.1'  # Local machine (localhost)
PORT = 5000          # Change this if the port is busy


# Store all connected clients and their usernames
clients = []
aliases = []


def broadcast(message, sender_socket=None):
    """Send the given message to all clients except the sender."""
    for client in clients:
        if client != sender_socket:
            try:
                client.send(message)
            except:
                print("[SERVER] Failed to send message to a client.")



def handle_client(client_socket):
    """Listen for messages from one client and share them with everyone."""
    
    while True:
        try:
            
            # Wait for incoming message bytes
            message_bytes = client_socket.recv(1024)
            if not message_bytes:
                raise ConnectionError  # Treat empty as a disconnect

            # Decode the raw message
            message_str = message_bytes.decode('utf-8').strip()

            # Look up the alias for this client_socket
            index = clients.index(client_socket)
            alias = aliases[index]

            # Combine the alias and the actual message for clarity
            full_message_str = f"{alias}: {message_str}"
            full_message_bytes = full_message_str.encode('utf-8')

            # Print it on the server for debugging
            print(f"[DEBUG] {full_message_str}")

            # Broadcast to other clients
            broadcast(full_message_bytes, sender_socket=client_socket)

            # Echo the labeled message back to the sender
            client_socket.send(full_message_bytes)


        except:
            # On error/disconnect, remove this client from the lists
            if client_socket in clients:
                index = clients.index(client_socket)
                alias = aliases[index]

                clients.pop(index)
                aliases.pop(index)
                client_socket.close()

                print(f"[SERVER] {alias} disconnected.")
                broadcast(f"[SERVER] {alias} left the chat.\n".encode('utf-8'))
            break



def receive_connections(server_socket):
    """Accept new connections and start a thread to handle each client."""
    while True:
        try:
            client_socket, address = server_socket.accept()
            print(f"[SERVER] New connection from {address}")

            # Request the alias from the client
            client_socket.send("ALIAS".encode('utf-8'))
            alias = client_socket.recv(1024).decode('utf-8').strip()

            if not alias:
                # If no alias is provided, close and ignore
                client_socket.close()
                continue

            # Track the client's alias and socket
            aliases.append(alias)
            clients.append(client_socket)

            print(f"[SERVER] {alias} joined the chat.")
            broadcast(f"[SERVER] {alias} joined the chat!\n".encode('utf-8'))

            client_socket.send("[SERVER] You are now connected!\n".encode('utf-8'))

            # Start a new thread to continuously handle messages from this client
            thread = threading.Thread(target=handle_client, args=(client_socket,))
            thread.start()

        except Exception as e:
            print(f"[SERVER] Error accepting connection: {e}")



def main():
    """Initialize the chat server on HOST:PORT and wait for new clients."""
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen()
    print(f"[SERVER] Listening on {HOST}:{PORT}...")
    receive_connections(server_socket)



if __name__ == "__main__":
    main()
