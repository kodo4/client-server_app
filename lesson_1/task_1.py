WORDS = ['разработка', 'сокет', 'декоратор']

for word in WORDS:
    print(f'{word} - type = {type(word)}')

unicode = {
    'разработка':
        '\u0440\u0430\u0437\u0440\u0430\u0431\u043e\u0442\u043a\u0430',
    'сокет':
        '\u0441\u043e\u043a\u0435\u0442',
    'декоратор':
        '\u0434\u0435\u043a\u043e\u0440\u0430\u0442\u043e\u0440'
}

for key in unicode:
    print(f'{unicode[key]} - type = {type(unicode[key])}, '
          f'длина - {len(unicode[key])}')
