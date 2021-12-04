import asyncio
from threading import Thread
from os import system
from datetime import datetime

from Socket import Socket
from User import User, register_user
from Room import Room, room_menu
from server import Server

class Client(Socket):
    def __init__(self, user):
        super(Client, self).__init__()
        self.user: User = user
        self.messages = ""
        self.encrypt_key = 10

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
            data = self.decrypt(data.decode('utf-8'))

            self.messages += f"({datetime.now().date()}): {data}\n"
            system('cls')
            print(self.messages)
    
    async def send_data(self, data=None) -> None:
        while True:
            data = await self.main_loop.run_in_executor(None, input, ">>> ")
            data = self.encrypt(data)
            await self.main_loop.sock_sendall(self.socket, data.encode("utf-8"))

    async def main(self):
        await asyncio.gather(
            self.main_loop.create_task(self.listen_socket()),
            self.main_loop.create_task(self.send_data()),
        )

    def encrypt(self, message):
        encrypted_message = ''
        for pos, symbol in enumerate(message):
            if pos % 2 == 0:
                encrypted_message += chr(ord(symbol) - self.encrypt_key)
            else:
                encrypted_message += chr(ord(symbol) + self.encrypt_key)
                
        return encrypted_message

    def decrypt(self, encrypted_message):
        decrypted_message = ''
        print(encrypted_message)
        for pos, symbol in enumerate(encrypted_message):
            if pos % 2 == 0:
                decrypted_message += chr(ord(str(symbol)) + self.encrypt_key)
            else:
                decrypted_message += chr(ord(str(symbol)) - self.encrypt_key)

        return decrypted_message

if __name__ == "__main__":
    user: User = register_user()
    if not user: quit(0)
    room: Room = room_menu()
    try:
        listen_amount = 5 if room.password else 10
        server = Server()
        server.set_up(room.IP_SERVER, room.port_server, listen_amount)
        server_thread = Thread(target=server.start)
        server_thread.start()
    
    except OSError:
        print("Подключение к серверу")

    client = Client(user)
    client.set_up(room.IP_SERVER, room.port_server)
    client.start()

    