import socket
import os

BUFFER_SIZE = 4096  # Fixed-size buffer for reading/writing data

# Define the server address and port
SERVER_IP = "2409:4071:6e18:71e5:2c99:b22f:4596:4b63"  # Replace with the server's IP address (IPv6)
SERVER_PORT = 12345

# Create a TCP socket
client_socket = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)

# Connect to the server
client_socket.connect((SERVER_IP, SERVER_PORT))

while True:
    # Get user input
    message = input("You: ")

    # Send the message to the server
    client_socket.send(message.encode('utf-8'))

    if message.lower() == "bye":
        break
    elif message.lower() == "sendfile":
        file_path = input("Enter the path of the file to send: ").strip('"')
        if not os.path.isfile(file_path):
            print("File not found.")
        else:
            # Get the file extension
            _, file_extension = os.path.splitext(file_path)

            # Send the file extension to the server
            client_socket.send(file_extension.encode('utf-8'))

            # Open the file and read its content in binary mode
            with open(file_path, 'rb') as file:
                while True:
                    file_data = file.read(BUFFER_SIZE)
                    if not file_data:
                        break
                    print(f"Sending {len(file_data)} bytes of data...")
                    client_socket.send(file_data)

            # Send the end signal to indicate file transmission completion
            client_socket.send(b'FILE_END')
            print("File sent successfully.")
    #else:
        # Receive and print the echo from the server
       # echo_message = client_socket.recv(BUFFER_SIZE).decode('utf-8')
       # print("Server: {}".format(echo_message))

# Close the client socket
client_socket.close()
