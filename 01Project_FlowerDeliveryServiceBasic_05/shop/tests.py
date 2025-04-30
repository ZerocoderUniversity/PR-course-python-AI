from django.test import TestCase
#
# # Create your tests here.
# strok = "shop/img/b1.jpg"
#
# for i in range(10):
#     sl_strok = strok[0:10] + str(i) + strok[11:15]
#     print(sl_strok)
from shop.models import Flower2, Order

print(Flower2.objects.all())
print(Order.objects.all())