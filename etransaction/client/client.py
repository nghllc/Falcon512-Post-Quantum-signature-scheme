import socket
import ssl

HOST = '127.0.0.1'
PORT = 9090

context = ssl.create_default_context()
context.check_hostname = False
context.load_verify_locations('client/server.crt')

with socket.create_connection((HOST, PORT)) as sock:
    with context.wrap_socket(sock, server_hostname=HOST) as ssock:
        ssock.sendall(b'Hello, World!')
        data = ssock.recv(1024)

print('Received:', data.decode())

