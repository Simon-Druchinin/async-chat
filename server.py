import os
import asyncio
from datetime import datetime
from Socket import Socket

from settings import IP_SERVER, PORT_SERVER, TXT_LOGS_PATH


class Server(Socket):
    def __init__(self):
        super(Server, self).__init__()
        self.clients = []
    
    def set_up(self, ip: str, port: int, listen_amount:int=5) -> None:
        self.socket.bind((ip, port))
        self.socket.listen(listen_amount)

        self.socket.setblocking(False)
    
    def _write_logs_to_txt(self, message):
        if os.stat(TXT_LOGS_PATH).st_size:
            with open(TXT_LOGS_PATH, 'r', encoding="utf-8") as read_file:
                lines = read_file.readlines()
            lines += f"[{datetime.now().date()}]: {message}\n"
        else:
            lines = f"[{datetime.now().date()}]: {message}\n"

        with open(TXT_LOGS_PATH, 'w', encoding="utf-8") as read_file:
            for line in lines:
                read_file.write(line)
    
    async def send_data(self, data: str) -> None:
        for client in self.clients: await self.main_loop.sock_sendall(client, data)

    async def listen_socket(self, listened_socket: object = None) -> None:
        while True:
            try:
                data = await self.main_loop.sock_recv(listened_socket, 2048)                
                await self.send_data(data)
            except ConnectionResetError:
                self.clients.remove(listened_socket)
                return

    async def accept_sockets(self) -> None:
        while True:
            client_socket, address = await self.main_loop.sock_accept(self.socket)
            self.clients.append(client_socket)

            message = f"{address[1]} connected"
            self._write_logs_to_txt(message)

            self.main_loop.create_task(self.listen_socket(client_socket))

    async def main(self):
        await self.main_loop.create_task(self.accept_sockets())

if __name__ == "__main__":
    server = Server()
    server.set_up(IP_SERVER, PORT_SERVER)

    server.start()
