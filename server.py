import socket


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.bind(("127.0.0.1", 3228))

server.listen()

while True:
    user_socket, address = server.accept()

    user_socket.send(f"{address[0]} connected".encode("utf-8"))

    data = user_socket.recv(2048)

    print(data.decode("utf-8"))
