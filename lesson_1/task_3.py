WORDS = ['attribute', 'класс', 'функция', 'type']


def str_to_byte(word):
    try:
        result = eval('b' + f'"{word}"')
        print(f'Word "{word}" can be write with b type')
        return result
    except SyntaxError:
        print('Error with word: ', word)
        print('bytes can only contain ASCII literal characters.')


for b_word in WORDS:
    str_to_byte(b_word)
    print(50 * '-')
