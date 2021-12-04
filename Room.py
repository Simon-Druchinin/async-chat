import os
import json
from threading import Thread

from server import Server
from settings import IP_SERVER, JSON_ROOM_PATH, PORT_SERVER


class Room():
    JSON_ROOM_PATH = JSON_ROOM_PATH
    IP_SERVER = IP_SERVER

    @staticmethod
    def check_password(password: str, port: str):
        rooms_list = Room.get_rooms_list()
        for room in rooms_list:
            if next(iter(room)) == str(port):
                room_password = room[str(port)]
        
        return password == room_password

    @staticmethod
    def is_port_exists(port: int) -> bool:
        rooms_list = Room.get_rooms_list()
        for room in rooms_list:
            if (next(iter(room)) == str(port)) or (port<1111 or port>9999):
                return True
        
        return False

    @staticmethod
    def get_rooms_list() -> list:
        rooms_list = []

        if os.stat(JSON_ROOM_PATH).st_size:
            with open(JSON_ROOM_PATH, "r", encoding="utf-8") as read_file:
                rooms_list = json.load(read_file)
            
        return rooms_list

    def __init__(self, port_server: str, password: str|None):
        self.port_server: int = int(port_server)
        self.password: str|None = password

        self.IP_SERVER: str = IP_SERVER
    
    def _write_to_json(self):
        if os.stat(JSON_ROOM_PATH).st_size:
            with open(JSON_ROOM_PATH, "r", encoding="utf-8") as json_file:
                data = json.load(json_file)
            
            for num, user in enumerate(data):
                if next(iter(user)) == self.port_server:
                    data[num] = {str(self.port_server): self.password}
                    break
            else:
                data.append({str(self.port_server): self.password})
        else:
            data = []
            data.append({str(self.port_server): self.password})
        
        with open(JSON_ROOM_PATH, "w", encoding="utf-8") as json_file:
            json.dump(data, json_file, ensure_ascii=False)


def room_menu():
    user_choice = ''

    while True:
        print("\nМеню:")
        print("1. Создать чат-комнату по паролю и порту\n2. Подключиться по порту и паролю\n3. Подключиться в чат со свободным доступом")
        user_choice = input("> ")
        if user_choice == "1":
            port = int(input("Введите порт для комнаты (от 1111 до 9999): "))
            if Room.is_port_exists(port):
                print("Такой порт уже занят!")
                continue

            password = input("Введите пароль для комнаты: ")

            room = Room(port, password)
            room._write_to_json()
            
            print("Комната успешно создана!")
            return room

        elif user_choice == "2":
            port = int(input("Введите порт для комнаты (от 1111 до 9999): "))
            if not Room.is_port_exists(port):
                print("Такого порта не существует!")
                continue

            password = input("Введите пароль для комнаты: ")

            if not Room.check_password(password, port):
                print("Пароль введён некорректно!")
                continue
            
            room = Room(port, password)

            return room
        
        elif user_choice == "3":
            room = Room(PORT_SERVER, None)

            return room
                
        else:
            print("Такой команды не существует")
