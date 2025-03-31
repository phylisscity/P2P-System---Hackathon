import asyncio



async def connect_to_server():
    """Connects to the server and sets up communication."""
    
    # Get a username (alias) from the user
    alias = input("Enter your chat name: ")


    # Connect to the server (127.0.0.1 is your local computer)
    try:
        reader, writer = await asyncio.open_connection('127.0.0.1', 5000)
    except ConnectionRefusedError:
        print("[ERROR] Could not connect to the server. Make sure it's running!")
        return


    # Server will ask for an alias first
    response = await reader.read(100)
    if response.decode('utf-8') == 'ALIAS':
        writer.write(alias.encode('utf-8'))  # Send alias
        await writer.drain()


    print("[CONNECTED] You are now in the chat. Type messages and press Enter to send!")



    async def receive_messages():
        """Keeps receiving and printing messages from the server."""
        while True:
            try:
                message = await reader.read(1024)  # Get message
                if not message:
                    print("[DISCONNECTED] Server is not responding.")
                    break
                print(message.decode('utf-8'))  # Print the message
            except:
                print("[ERROR] Lost connection to server.")
                break




    async def send_messages():
        """Reads user input and sends it to the server."""
        while True:
            message = input("")  # Get user input
            writer.write(message.encode('utf-8'))  # Send to server
            await writer.drain()

    # Run both sending and receiving at the same time
    await asyncio.gather(receive_messages(), send_messages())



if __name__ == "__main__":
    asyncio.run(connect_to_server())  # Start client
