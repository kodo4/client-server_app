WORDS = ['разработка', 'администрирование', 'protocol', 'standard']

for word in WORDS:
    print(f'{word} - type: {type(word)}')
    enc_word = word.encode('utf-8')
    print(f'{enc_word} - type: {type(enc_word)}')
    dec_word = enc_word.decode('utf-8')
    print(f'{dec_word} - type: {type(dec_word)}')
    print(25 * '-')
