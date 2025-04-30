from shop.models import Flower

def add_flower(name, price, description, image_link):
    new_flower = Flower(name=name, price=price, description=description, image_link=image_link)
    new_flower.save()

add_flower('Букет 1', 1000, 'Прекрасная корзинка цветов', 'shop/img/b1.jpg')