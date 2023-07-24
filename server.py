import socket
import threading

BUFFER_SIZE = 4096  # Fixed-size buffer for reading/writing data

def handle_client(client_socket, client_address):
    print(f"Accepted connection from {client_address}")
    while True:
        data = client_socket.recv(BUFFER_SIZE).decode('utf-8')
        if not data:
            break
        if data.lower() == 'bye':
            client_socket.send("Goodbye".encode('utf-8'))
            print(f"Connection with {client_address} closed.")
            client_socket.close()
            return  # Exit the function and thread

        if data.lower() == 'sendfile':
            receive_file(client_socket)
        else:
            if data.lower() != 'sendfile':  # Handle "sendfile" without echoing
                print(f"Received message from {client_address}: {data}")
                # Echo the message back to the client
                client_socket.send(data.encode('utf-8'))

def receive_file(client_socket):
    # Receive the file extension from the client
    file_extension = client_socket.recv(BUFFER_SIZE).decode('utf-8')
    file_path = f"received_file{file_extension}"

    client_socket.send("Ready to receive file".encode('utf-8'))
    file_data = b""
    while True:
        data = client_socket.recv(BUFFER_SIZE)
        if not data:
            break
        if data.endswith(b'FILE_END'):
            file_data += data[:-8]  # Exclude the 'FILE_END' marker
            break
        file_data += data

    # Save the file with the correct extension in binary mode
    with open(file_path, 'wb') as file:
        file.write(file_data)

    print(f"File received and saved as '{file_path}'.")
    print(f"Received {len(file_data)} bytes of data.")

    # Check if the received file is a text file (.txt) and print its content if it's not too large
    if file_extension == ".txt":
        if len(file_data) <= BUFFER_SIZE:
            with open(file_path, 'r') as file:
                file_content = file.read()
                print("\nReceived file content:\n")
                print(file_content)
                print("\nEnd of file content\n")
        else:
            print(f"The file '{file_path}' is too large to display its content on the terminal.")

def start_server(host, port):
    server_socket = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((host, port))
    server_socket.listen(5)
    print(f"Server listening on {host}:{port}")

    while True:
        client_socket, client_address = server_socket.accept()
        client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
        client_thread.start()

if __name__ == "__main__":
    HOST = "::1"
    PORT = 12345

    start_server(HOST, PORT)


