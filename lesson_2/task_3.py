import yaml

users = ['kodo', 'apt']
year = 2022
valute = {'YEN': chr(165),
          'GBP': chr(163)}
DATA_TO_YAML = {'users': users,
                'year': year,
                'valute': valute}

with open('file.yaml', 'w', encoding='utf-8') as f:
    yaml.dump(DATA_TO_YAML, f, default_flow_style=False,
              sort_keys=False, allow_unicode=True)

with open('file.yaml', encoding='utf-8') as f_r:
    data_from_yaml = yaml.load(f_r, Loader=yaml.FullLoader)

print(DATA_TO_YAML == data_from_yaml)
