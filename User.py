import os
import re
import json
from typing import NoReturn

from settings import JSON_USER_PATH


class User:
    JSON_USER_PATH = JSON_USER_PATH

    @staticmethod
    def check_password(password: str, password_repeat: str):
        if not re.match(r".{8,}", password):
                return False

        return password == password_repeat
    
    @staticmethod
    def sign_up(username: str, password: str):
        user_hash = {"username": username,
                    "password": password,
                    "watched_films": [],
                    "films_to_watch": [],
                    }
        user = User(user_hash)
        user._write_to_json()

        return user

    @staticmethod
    def is_signed_up(username: str) -> bool:
        users_list = User.get_users_list()
        for user in users_list:
            if username == next(iter(user)):
                return True

        return False
    
    @staticmethod
    def log_in(username: str, password: str):
        users_list = User.get_users_list()
        for user in users_list:
            if username == next(iter(user)):
                user_hash = user[username]
                user_hash["username"] = username
                user = User(user_hash)
        
                if user.password == password:
                    return user
        
        return None

    @staticmethod
    def get_users_list() -> list:
        users_list = []

        if os.stat(JSON_USER_PATH).st_size:
            with open(JSON_USER_PATH, "r", encoding="utf-8") as read_file:
                users_list = json.load(read_file)
            
        return users_list

    def __init__(self, user_hash: dict):
        self.username: str = user_hash["username"]
        self.password: str = user_hash["password"]
    
    def __get_user_hash(self):
        user_hash = {
            self.username: {
                "password": self.password,
            }
        }
        
        return user_hash

    def _write_to_json(self) -> NoReturn:
        if os.stat(JSON_USER_PATH).st_size:
            with open(JSON_USER_PATH, "r", encoding="utf-8") as json_file:
                data = json.load(json_file)
            
            for num, user in enumerate(data):
                if next(iter(user)) == self.username:
                    data[num] = self.__get_user_hash()
                    break
            else:
                data.append(self.__get_user_hash())
        else:
            data = []
            data.append(self.__get_user_hash())
        
        with open(JSON_USER_PATH, "w", encoding="utf-8") as json_file:
            json.dump(data, json_file, ensure_ascii=False)


def register_user():
    user_choice = ''

    while user_choice != "3":
        print("\nРегистрация:")
        print("1. Зарегистрироваться\n2. Войти\n3. Выход")
        user_choice = input("> ")
        if user_choice == "1":
            username = input("Придумайте никнейм: ")
            if User.is_signed_up(username):
                print("\nНикнейм уже занят!\nПридумайте другой!\n")
                continue

            password = input("Введите пароль: ")
            password_repeat = input("Повторите пароль: ")

            if not User.check_password(password, password_repeat):
                print(  "Пароли не совпадают или длина пароля "\
                        "меньше 8-ми символов")
                continue
            user = User.sign_up(username, password)
            
            return user

        elif user_choice == "2":
            username = input("Введите никнейм: ")
            if not User.is_signed_up(username):
                print("Пользователя с таким никнеймом не существует!")
                continue
            
            password = input("Введите пароль: ")
            user = User.log_in(username, password)
            if user:
                return user
            else:
                print("Пароль введён некорректно!")
                
        elif user_choice != "3":
            print("Такой команды не существует")
    
    return None