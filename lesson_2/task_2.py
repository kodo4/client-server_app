import json
from datetime import datetime


def write_order_to_json(item, quantity, price, buyer):
    with open('orders.json', encoding='utf-8') as f:
        obj = json.load(f)
        obj['orders'] = [item, quantity, price, buyer, datetime.now()]
    with open('orders.json', 'w', encoding='utf-8') as f_w:
        json.dump(obj, f_w, indent=4, default=str, ensure_ascii=False)


write_order_to_json('кружка', 5, 500, 'Roman')
