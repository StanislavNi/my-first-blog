"""Classes for getting user's text"""
import requests
from bs4 import BeautifulSoup
import os


class HandlerException(Exception):
    pass


class InputInterface(object):
    """
    Parent class for
    user's input classes
    """
    def __init__(self, users_text):
        self.users_text = users_text.strip()

    def get_text(self):
        raise NotImplementedError

    def is_valid(self):
        raise NotImplementedError


class InputFileText(InputInterface):
    """
    Get text from user's
    file
    """
    def get_text(self):
        try:
            if os.stat(self.users_text).st_size > 0:
                f = open(self.users_text, 'r')
                return f.read()
            return False
        except FileExistsError:
            raise HandlerException('Несуществующий файл')

    def is_valid(self):
        if self.users_text.endswith('.txt'):
            return True


class InputUrlText(InputInterface):
    """
    Get text from user's
    URL
    """
    def get_text(self):
        try:
            r = requests.get(self.users_text, timeout=1)
            if r.status_code == requests.codes.ok:
                soup = BeautifulSoup(r.content, 'html.parser')
                return ''.join(c for c in soup.text)
        except requests.exceptions.InvalidURL:
            raise HandlerException('Сайта не существует')
        except requests.exceptions.ConnectionError:
            raise HandlerException('Нет доступа к интернету')

    def is_valid(self):
        if self.users_text.startswith('http'):
            return True


class ConsoleText(InputInterface):
    """
    Get text from user's
    console
    """
    users_text = ''

    def get_text(self):
        if self.users_text == ' ':
            return 'Вы ввели пустую строку'
        return self.users_text

    def is_valid(self):
        return True


class InputHandlers(object):
    input_handlers = [
        InputFileText,
        InputUrlText,
        ConsoleText,
    ]

    def parse(self, user_input):
        text = None
        for handler_cls in self.input_handlers:
            handler_instance = handler_cls(user_input)
            if handler_instance.is_valid():
                text = handler_instance.get_text()
                break
        return text
