import socket
import threading
import os

# Server configurations
SERVER_HOST = '127.0.0.1'  # Replace 'server_ip_or_domain' with the actual server's IP address or domain name
SERVER_PORT = 12345
BUFFER_SIZE = 4096  # Increased buffer size for handling files

def receive_messages(client_socket):
    while True:
        try:
            data = client_socket.recv(BUFFER_SIZE)
            if not data:
                print("Connection closed by the server.")
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

                print(f"Received {filename} ({file_size} bytes).")
            else:
                print(data.decode())

        except ConnectionResetError:
            print("Server has closed the connection.")
            break

def send_file(client_socket, file_path):
    # Send file identifier to the server
    filename = os.path.basename(file_path)
    client_socket.sendall(f"FILE:{filename}".encode())

    # Send file size to the server
    file_size = os.path.getsize(file_path)
    client_socket.sendall(str(file_size).encode())

    # Send the file data in chunks
    with open(file_path, 'rb') as file:
        while True:
            data = file.read(BUFFER_SIZE)
            if not data:
                break
            client_socket.sendall(data)

def main():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((SERVER_HOST, SERVER_PORT))

    # Receive server's initial message (Please enter your nickname)
    print(client_socket.recv(BUFFER_SIZE).decode(), end="")
    nickname = input()
    client_socket.sendall(nickname.encode())

    # Start a thread to receive messages from the server
    receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
    receive_thread.start()

    try:
        while True:
            message = input()
            if message.lower() == "exit":
                client_socket.sendall(message.encode())
                break

            # Check if the message starts with "/file" indicating file transfer
            if message.startswith("/file"):
                _, file_path = message.split(" ", 1)
                send_file(client_socket, file_path)
            else:
                client_socket.sendall(message.encode())

    except KeyboardInterrupt:
        pass

    finally:
        client_socket.close()

if __name__ == "__main__":
    main()
import socket
import threading
import os

# Server configurations
SERVER_HOST = 'server_ip_or_domain'  # Replace 'server_ip_or_domain' with the actual server's IP address or domain name
SERVER_PORT = 12345
BUFFER_SIZE = 4096  # Increased buffer size for handling files

def receive_messages(client_socket):
    while True:
        try:
            data = client_socket.recv(BUFFER_SIZE)
            if not data:
                print("Connection closed by the server.")
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

                print(f"Received {filename} ({file_size} bytes).")
            else:
                print(data.decode())

        except ConnectionResetError:
            print("Server has closed the connection.")
            break

def send_file(client_socket, file_path):
    # Send file identifier to the server
    filename = os.path.basename(file_path)
    client_socket.sendall(f"FILE:{filename}".encode())

    # Send file size to the server
    file_size = os.path.getsize(file_path)
    client_socket.sendall(str(file_size).encode())

    # Send the file data in chunks
    with open(file_path, 'rb') as file:
        while True:
            data = file.read(BUFFER_SIZE)
            if not data:
                break
            client_socket.sendall(data)

def main():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((SERVER_HOST, SERVER_PORT))

    # Receive server's initial message (Please enter your nickname)
    print(client_socket.recv(BUFFER_SIZE).decode(), end="")
    nickname = input()
    client_socket.sendall(nickname.encode())

    # Start a thread to receive messages from the server
    receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
    receive_thread.start()

    try:
        while True:
            message = input()
            if message.lower() == "exit":
                client_socket.sendall(message.encode())
                break

            # Check if the message starts with "/file" indicating file transfer
            if message.startswith("/file"):
                _, file_path = message.split(" ", 1)
                send_file(client_socket, file_path)
            else:
                client_socket.sendall(message.encode())

    except KeyboardInterrupt:
        pass

    finally:
        client_socket.close()

if __name__ == "__main__":
    main()
