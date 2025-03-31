# P2P Chat Framework (Phase 1)

This is a simple peer-to-peer (P2P) chat system built in Python using **sockets** and **threading/asyncio**.

For now, it works like a basic client-server chat room.  
Each client connects to the server and can send messages to everyone else.

---

## 🚀 How it works

- **Server (`server.py`)**
  - Listens for new client connections.
  - Keeps track of all connected users.
  - Broadcasts messages from one client to everyone else.
  - Removes users when they disconnect.

- **Client (`client.py`)**
  - Connects to the server and chooses a chat name (alias).
  - Can send messages and receive messages at the same time.
  - Automatically leaves the chat if disconnected.

---

## 📝 How to Run

1. **Clone this repo**
    ```bash
    git clone https://github.com/phylisscity/P2P-System---Hackathon.git
    cd P2P-System---Hackathon
    ```

2. **Run the server**  
    Open a terminal window and run:
    ```bash
    python server.py
    ```

3. **Run the client**  
    In another terminal window (or multiple), run:
    ```bash
    python client.py
    ```

4. **Start chatting!**
    - Enter an alias (your chat name) when prompted.
    - Type messages and press Enter to send.
    - All messages will be shared with everyone connected.

---

## 📌 Requirements

- Python 3.x  
  No external libraries needed (just Python's built-in `socket`, `threading`, and `asyncio` modules).

---

## 🎯 Next Steps (Future Improvements)

Coming soon:
- `/exit` command → leave the chat gracefully.
- `/users` command → see who’s online.
- Private messaging between users.
- Secure message encryption.
