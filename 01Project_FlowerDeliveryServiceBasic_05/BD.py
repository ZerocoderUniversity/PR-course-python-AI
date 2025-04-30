import sqlite3

conn = sqlite3.connect('db.sqlite3')
cur = conn.cursor()

# cur.execute("DELETE FROM shop_flower2 WHERE id>?", (0,))
# conn.commit()
#
cur.execute(f"INSERT INTO shop_flower2 (id, name, price, description, image_link) VALUES "
            f"(1, 'Букет 1', 1000, 'Прекрасная корзинка цветов', 'shop/img/b1.jpg')")
cur.execute(f"INSERT INTO shop_flower2 (id, name, price, description, image_link) VALUES "
            f"(2, 'Букет 2', 1000, 'Этот букет очень красивый', 'shop/img/b2.jpg')")
cur.execute(f"INSERT INTO shop_flower2 (id, name, price, description, image_link) VALUES "
            f"(3, 'Букет 3', 800, 'Разные красивые цветочки', 'shop/img/b3.jpg')")
cur.execute(f"INSERT INTO shop_flower2 (id, name, price, description, image_link) VALUES "
            f"(4, 'Букет 4', 2500, 'Красные розы 25 штук', 'shop/img/b4.jpg')")
cur.execute(f"INSERT INTO shop_flower2 (id, name, price, description, image_link) VALUES "
            f"(5, 'Букет 5', 2000, 'Букет белых роз', 'shop/img/b5.jpg')")
cur.execute(f"INSERT INTO shop_flower2 (id, name, price, description, image_link) VALUES "
            f"(6, 'Букет 6', 1500, 'Что-то очень красивое', 'shop/img/b6.jpg')")
cur.execute(f"INSERT INTO shop_flower2 (id, name, price, description, image_link) VALUES "
            f"(7, 'Букет 7', 800, 'Ромашки - просто и со вкусом', 'shop/img/b7.jpg')")
cur.execute(f"INSERT INTO shop_flower2 (id, name, price, description, image_link) VALUES "
            f"(8, 'Букет 8', 1200, 'Большой букет ромашек', 'shop/img/b8.jpg')")
cur.execute(f"INSERT INTO shop_flower2 (id, name, price, description, image_link) VALUES "
            f"(9, 'Букет 9', 1350, 'Очень красиво смотрится', 'shop/img/b9.jpg')")
conn.commit()

#cur.execute(f"SELECT * FROM sqlite_master WHERE type = 'table'")
#cur.execute(f"SELECT * FROM shop_flower2")
#cur.execute(f"SELECT * FROM shop_order")
#cur.execute(f"SELECT * FROM shop_order_products")
#cur.execute(f"SELECT * FROM shop_shopping")

# cur.execute("DELETE FROM shop_shopping WHERE id>?", (0,))
# conn.commit()
# cur.execute(f"SELECT * FROM shop_shopping")

#cur.execute("DROP TABLE shop_shopping")
#conn.commit()
# cur.execute("""CREATE TABLE IF NOT EXISTS shop_shopping (
#     id INTEGER PRIMARY KEY AUTOINCREMENT,
#     products TEXT,
#     status BOOLEAN)""")
# conn.commit()
cur.execute(f"SELECT * FROM sqlite_master WHERE type = 'table'")

#cur.execute(f"SELECT * FROM shop_select_shop")

names = [description[0] for description in cur.description]
print (names)
rows = cur.fetchall()
for row in rows:
    print(row)
conn.close()
