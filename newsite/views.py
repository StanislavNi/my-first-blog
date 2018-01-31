"""Script for working with the user's text"""
from django.http import HttpResponse
from newsite.handlers import InputHandlers, HandlerException


def text_info(text):
    stored_text = []

    def store_text(*args):
        stored_text.extend(args)
        return ' '.join(map(str, stored_text))

    # Count the length of the text
    store_text('Длина строки равна: ', len(text), '</br>')
    string_list = text.split()

    # Count the number of letters
    store_text('Количество слов в тексте равно: ', len(string_list), '</br>')

    # Count the number of numerals
    num = ([int(i) for i in string_list if i.isdigit()])
    store_text('Количество чисел в тексте равно:', len(num), '</br>')

    # Divide the text by strings with the length 25 symbols
    def max_string(s, n):
        """
        Divide 's'(user's text)
        by 'n'(string length)
        """
        return [text[i:i + n] for i in range(0, len(text), n)]

    store_text('Вывод текста по 25 символов: ')
    for s in max_string(text, 25):
        store_text(s, '</br>')

    def reverse(text):
        """
        Reverse user's text
        from the last symbol
        to the first
        """
        return text[::-1]

    reversed_text = reverse(text)
    # Print reversed strings with the length 25 symbols
    store_text('Вывод текста по 25 символов с конца: ')
    divided_reversed = (
        [reversed_text[i:i + 25] for i in
         range(0, len(reversed_text), 25)])
    for a in divided_reversed:
        store_text(a, '</br>')

    return stored_text


def print_string(request):
    text = InputHandlers().parse(request.GET.get('text') or 'temp text')
    result = text_info(text)
    return HttpResponse(result)
