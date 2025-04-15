import asyncio



async def connect_to_server():
    """Establish a connection with the server and manage chat communication."""
    
    # Request a chat name.
    alias = input("Enter chat name: ")
    
    
    
    # Attempt to connect to the server.
    try:
        reader, writer = await asyncio.open_connection('127.0.0.1', 5000)  #make sure to update to match server's port
    except ConnectionRefusedError:
        print("[ERROR] Server connection failed.")
        return



    # Receive alias prompt from the server and send the alias.
    response = await reader.read(100)
    if response.decode('utf-8') == "ALIAS":
        writer.write(alias.encode('utf-8'))
        await writer.drain()

    print("[CONNECTED] Connected to chat. Type to send messages.")

    async def receive_messages():
        
        """Receive and print incoming messages from the server."""
        while True:
            try:
                message = await reader.read(1024)
                if not message:
                    print("[DISCONNECTED] Server closed connection.")
                    break
                print(message.decode('utf-8').strip())
            except Exception as e:
                print(f"[ERROR] Lost connection: {e}")
                break


    async def send_messages():
        """Send user messages to the server using nonblocking input."""
        while True:
            
            # Asynchronously run the built-in input() in a separate thread.
            message = await asyncio.to_thread(input, "")
            writer.write(message.encode('utf-8'))
            await writer.drain()


    # Run both receive and send concurrently.
    await asyncio.gather(receive_messages(), send_messages())

def main():
    """Entry point for the chat client."""
    asyncio.run(connect_to_server())

if __name__ == "__main__":
    main()
