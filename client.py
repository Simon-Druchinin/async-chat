from Socket import Socket
from threading import Thread

from settings import IP_SERVER, PORT_SERVER

class Client(Socket):
    def __init__(self):
        super(Client, self).__init__()

    def set_up(self, ip:str, port:int) -> None:
        self.connect((ip, port))

        listen_thread = Thread(target=self.listen_socket)
        listen_thread.start()

        send_thread = Thread(target=self.send_data)
        send_thread.start()
    
    def listen_socket(self, listened_socket: object=None) -> None:
        while True:
            data = self.recv(2048)
            print(data.decode("utf-8"))
    
    def send_data(self) -> None:
        while True:
            self.send(input(">>> ").encode("utf-8"))

if __name__ == "__main__":
    client = Client()
    client.set_up(IP_SERVER, PORT_SERVER)
