import asyncio
from socket import socket, AF_INET, SOCK_STREAM


class Socket():
    def __init__(self):
        self.socket = socket(AF_INET, SOCK_STREAM)
        self.main_loop = asyncio.get_event_loop()
    
    async def send_data(self):
        raise NotImplementedError()

    async def listen_socket(self):
        raise NotImplementedError()
    
    async def main(self): 
        raise NotImplementedError()
    
    def start(self):
        self.main_loop.run_until_complete(self.main())

    def set_up(self):
        raise NotImplementedError()