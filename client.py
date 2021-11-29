import socket


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client.connect(("127.0.0.1", 3228))

while True:
    data = client.recv(2048)

    print(data.decode("utf-8"))

    client.send(input(">>> ").encode("utf-8"))
