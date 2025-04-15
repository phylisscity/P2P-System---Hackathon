import asyncio



async def connect_to_server():
    """Connect to the server and start the chat session."""
    
    
    # Ask the user for their chat name
    alias = input("Enter your chat name: ")


    # Try to connect to the server
    try:
        
        # localhost (127.0.0.1) means your own computer
        reader, writer = await asyncio.open_connection('127.0.0.1', 5000)
    except ConnectionRefusedError:
        print("[ERROR] Could not connect to the server. Make sure it's running!")
        return



    # Server should ask for ALIAS before anything
    response = await reader.read(100)
    if response.decode('utf-8') == 'ALIAS':
        # Send the alias (your username) to the server
        writer.write(alias.encode('utf-8'))
        await writer.drain()

    print("[CONNECTED] You are now in the chat. Type messages and press Enter to send!")



    # Function to keep listening for incoming messages
    async def receive_messages():
        while True:
            try:
                message = await reader.read(1024)
                if not message:
                    print("[DISCONNECTED] Server is not responding.")
                    break
                print(message.decode('utf-8'))  # Show message to user
            except:
                print("[ERROR] Lost connection to server.")
                break



    # Function to send messages typed by the user
    async def send_messages():
        while True:
            message = input("")  # Wait for user input
            writer.write(message.encode('utf-8'))  # Send it
            await writer.drain()



    # Run both message sending and receiving at the same time
    await asyncio.gather(receive_messages(), send_messages())



# This function runs if the user installed the package via pip
def main():
    
    # Temporary function for testing install
    # This will be replaced by the actual chat logic
    asyncio.run(connect_to_server())
