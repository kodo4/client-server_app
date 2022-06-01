import chardet
WORDS = ['сетевое программирование', 'сокет', 'декоратор']

f = open('test_file.txt', 'w', encoding='utf-8')
for word in WORDS:
    f.write(word + '\n')
f.close()

with open('test_file.txt', 'rb') as f:
    content = f.read()
encoding = chardet.detect(content)['encoding']

with open('test_file.txt', 'r', encoding=encoding) as f:
    for line in f:
        print(line, end='')
