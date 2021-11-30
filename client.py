import asyncio
from os import system
from datetime import datetime

from Socket import Socket
from settings import IP_SERVER, PORT_SERVER

class Client(Socket):
    def __init__(self):
        super(Client, self).__init__()
        self.messages = ""

    def set_up(self, ip:str, port:int) -> None:
        try:
            self.socket.connect((ip, port))
        except ConnectionRefusedError:
            print("Server is not online right now :(")
            exit(0)

        self.socket.setblocking(False)
    
    async def listen_socket(self, listened_socket: object=None) -> None:
        while True:
            data = await self.main_loop.sock_recv(self.socket, 2048)

            self.messages += f"{datetime.now().date()}: {data.decode('utf-8')}\n"
            system('cls')
            print(self.messages)
    
    async def send_data(self, data=None) -> None:
        while True:
            data = await self.main_loop.run_in_executor(None, input, ">>> ")
            await self.main_loop.sock_sendall(self.socket, data.encode("utf-8"))

    async def main(self):
        await asyncio.gather(
            self.main_loop.create_task(self.listen_socket()),
            self.main_loop.create_task(self.send_data()),
        )


if __name__ == "__main__":
    client = Client()
    client.set_up(IP_SERVER, PORT_SERVER)

    client.start()
