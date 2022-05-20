import chardet
import csv
import re

FILES = ['info_1.txt', 'info_2.txt', 'info_3.txt']


def get_data(files):
    main_data = [['Изготовитель системы',
                 'Название ОС',
                 'Код продукта',
                 'Тип системы']]
    os_prod_list = []
    os_name_list = []
    os_code_list = []
    os_type_list = []
    for file in files:
        with open(file, 'rb') as f:
            content = f.read()
            encoding = chardet.detect(content)['encoding']
        with open(file, 'r', encoding=encoding) as f_n:
            content = csv.reader(f_n)
            for row in content:
                re_os_prod = re.match('Изготовитель системы:\s+', row[0])
                re_os_name = re.match('Название ОС:\s+', row[0])
                re_os_code = re.match('Код продукта:\s+', row[0])
                re_os_type = re.match('Тип системы:\s+', row[0])
                if re_os_prod:
                    os_prod = row[0]
                    os_prod_list.append(os_prod[int(re_os_prod.end()):])
                if re_os_name:
                    os_name = row[0]
                    os_name_list.append(os_name[int(re_os_name.end()):])
                if re_os_code:
                    os_code = row[0]
                    os_code_list.append(os_code[int(re_os_code.end()):])
                if re_os_type:
                    os_type = row[0]
                    os_type_list.append(os_type[int(re_os_type.end()):])
    for i in range(len(files)):
        main_data.append([os_prod_list[i], os_name_list[i], os_code_list[i],
                         os_type_list[i]])
    return main_data, encoding


def write_to_csv(files):
    main_data, encoding = get_data(files)
    with open('data_write.csv', 'w', encoding='utf-8') as f:
        F_WRITER = csv.writer(f)
        for row in main_data:
            F_WRITER.writerow(row)


write_to_csv(FILES)
