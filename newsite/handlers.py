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
    def get_text(self):
        raise NotImplementedError

    def is_valid(self, users_text):
        raise NotImplementedError


class InputFileText(InputInterface):
    """
    Get text from user's
    file
    """
    _filepath = None

    def get_text(self):
        try:
            if os.stat(self._filepath).st_size > 0:
                f = open(self._filepath, 'r')
                return f.read()
            return False
        except FileExistsError:
            raise HandlerException('Несуществующий файл')

    def is_valid(self, users_text):
        if users_text.endswith('.txt'):
            self._filepath = users_text
            return True



class InputUrlText(InputInterface):
    """
    Get text from user's
    URL
    """

    def get_text(self):
        try:
            r = requests.get(self.users_text, timeout=1)
        except requests.exceptions.InvalidURL:
            raise HandlerException('Сайта не существует')
        except requests.exceptions.ConnectionError:
            raise HandlerException('Нет доступа к интернету')

    def html_parse(self):
        r = requests.get(self.users_text, timeout=1)
        if r.status_code == requests.codes.ok:
            soup = BeautifulSoup(r.content, 'html.parser')
            return '\n'+ ''.join(c for c in soup.text)
        else:
            raise HandlerException('Невозможно отобразить страницу')

    def is_valid(self, users_text):
        users_text = users_text.strip()
        if users_text.startswith('http'):
            self.users_text = users_text
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

    def is_valid(self, users_text):
        self.users_text = users_text
        return True


class InputHandlers(object):
    input_handlers = [
        InputFileText(),
        InputUrlText(),
        ConsoleText(),
    ]

    def parse(self, user_input):
        text = None
        for editor in self.input_handlers:
            if editor.is_valid(user_input):
                text = editor.get_text()
                break
        return text
