import json
from datetime import datetime


def save_order_details(order_id, customer_name, items, total_price):
    # Создаем словарь с деталями заказа
    order_details = {
        "order_id": order_id,
        "customer_name": customer_name,
        "items": items,
        "total_price": total_price,
        "order_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    # Записываем словарь в файл в формате JSON
    with open('orders.json', 'a') as file:
        file.write(json.dumps(order_details) + '\n')

    print("Order details saved successfully.")