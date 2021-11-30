import asyncio
from Socket import Socket

from settings import IP_SERVER, PORT_SERVER


class Server(Socket):
    def __init__(self):
        super(Server, self).__init__()
        self.clients = []
    
    def set_up(self, ip: str, port: int) -> None:
        self.socket.bind((ip, port))
        self.socket.listen()

        self.socket.setblocking(False)
    
    async def send_data(self, data: str) -> None:
        for client in self.clients: await self.main_loop.sock_sendall(client, data)

    async def listen_socket(self, listened_socket: object = None) -> None:
        while True:
            data = await self.main_loop.sock_recv(listened_socket, 2048)
            print(f"User sent {data}")
            await self.send_data(data.encode('utf-8'))

    async def accept_sockets(self) -> None:
        while True:
            client_socket, address = await self.main_loop.sock_accept(self.socket)
            self.clients.append(client_socket)

            print(f"{address[1]} connected")

            self.main_loop.create_task(self.listen_socket(client_socket))

    async def main(self):
        await self.main_loop.create_task(self.accept_sockets())

if __name__ == "__main__":
    server = Server()
    server.set_up(IP_SERVER, PORT_SERVER)
    
    server.start()