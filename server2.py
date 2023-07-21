import socket
import threading
import os

# Server configurations
SERVER_HOST = '127.0.0.1'  # Listen on all available interfaces
SERVER_PORT = 12345
BUFFER_SIZE = 4096  # Increased buffer size for handling files

clients = {}  # Store client sockets and nicknames

def broadcast(message, sender_socket):
    """Send a message to all connected clients except the sender."""
    for client_socket in clients:
        if client_socket != sender_socket:
            try:
                client_socket.sendall(message)
            except:
                # Remove the client socket if the send fails
                remove_client(client_socket)

def remove_client(client_socket):
    """Remove a client socket from the list of clients."""
    if client_socket in clients:
        nickname = clients[client_socket]
        print(f"Connection closed by {nickname}.")
        client_socket.close()
        del clients[client_socket]
        broadcast(f"{nickname} has left the chat.".encode(), None)

def handle_client(client_socket):
    """Handle messages and file transfers from a connected client."""
    try:
        # Request and store the client's nickname
        client_socket.sendall("Please enter your nickname: ".encode())
        nickname = client_socket.recv(BUFFER_SIZE).decode()
        clients[client_socket] = nickname
        print(f"{nickname} has joined the chat.")
        broadcast(f"{nickname} has joined the chat.".encode(), client_socket)

        while True:
            data = client_socket.recv(BUFFER_SIZE)
            if not data:
                remove_client(client_socket)
                break

            # Check if the received data is a file
            if data.startswith(b"FILE:"):
                filename = data[5:].decode()
                file_size = int(client_socket.recv(BUFFER_SIZE).decode())

                # Receive the file data in chunks and save it
                with open(filename, 'wb') as file:
                    received_data = 0
                    while received_data < file_size:
                        data = client_socket.recv(BUFFER_SIZE)
                        file.write(data)
                        received_data += len(data)

                print(f"Received {filename} from {nickname} ({file_size} bytes).")
                broadcast(f"{nickname} sent a file: {filename}".encode(), client_socket)
            else:
                message = f"{nickname}: {data.decode()}"
                print(message)
                broadcast(message.encode(), client_socket)

    except ConnectionResetError:
        remove_client(client_socket)

def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((SERVER_HOST, SERVER_PORT))
    server_socket.listen(5)
    print(f"Listening on {SERVER_HOST}:{SERVER_PORT}")

    try:
        while True:
            client_socket, client_addr = server_socket.accept()
            print(f"Connection established with {client_addr[0]}:{client_addr[1]}")
            client_thread = threading.Thread(target=handle_client, args=(client_socket,))
            client_thread.start()
    except KeyboardInterrupt:
        pass
    finally:
        server_socket.close()

if __name__ == "__main__":
    main()
