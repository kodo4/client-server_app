WORDS = ['class', 'function', 'method']


def str_to_byte(word):
    result = eval('b' + f'"{word}"')
    return result


for b_word in WORDS:
    print(f'type: {type(str_to_byte(b_word))}, word: {str_to_byte(b_word)}, '
          f'len: {len(str_to_byte(b_word))}')
