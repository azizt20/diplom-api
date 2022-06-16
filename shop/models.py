from django.db import models
import datetime
from django.urls import reverse_lazy
# from django.utils.translation import gettext as _

today = datetime.date.today()


class PicturesMedicine(models.Model):
    image = models.ImageField(upload_to=f'medicine_pictures/{today.year}-{today.month}-{today.month}/',
                              null=True, blank=True)


class TypeProduct(models.Model):
    sub = models.ForeignKey('self', on_delete=models.RESTRICT, null=True, blank=True)
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to=f'types/', null=True, blank=True)
    icon = models.ImageField(upload_to=f'types/icons/', null=True, blank=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    image = models.ImageField(upload_to=f'medicine/', null=True, blank=True)
    pictures = models.ManyToManyField(PicturesMedicine, blank=True)
    name = models.CharField(max_length=224)
    title = models.CharField(max_length=224)
    order_count = models.IntegerField(default=0)
    description = models.TextField(null=True, blank=True)
    quantity = models.IntegerField(default=0)
    review = models.IntegerField(default=0)
    weight = models.FloatField(default=0)
    type_medicine = models.ForeignKey(TypeProduct, on_delete=models.RESTRICT, null=True)
    cost = models.IntegerField(null=True)
    discount = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now=True, null=True)
    gpu = models.CharField(max_length=224,null=True, blank=True)
    cpu = models.CharField(max_length=224,null=True, blank=True)
    power = models.CharField(max_length=224,null=True, blank=True)
    display = models.CharField(max_length=224,null=True, blank=True)
    ram = models.CharField(max_length=224,null=True, blank=True)

    def __str__(self):
        return self.name


class CartModel(models.Model):
    TYPE = (
        (1, 'active'),
        (2, 'done'),
    )
    user = models.ForeignKey('account.UserModel', on_delete=models.SET_NULL, null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.RESTRICT)
    amount = models.IntegerField(default=1)
    status = models.SmallIntegerField(default=1, choices=TYPE)

    @property
    def get_total_price(self):
        return self.product.cost * self.amount


PAYMENT_TYPES = (
    (1, 'Оплата при доставке'),
    (2, 'Кредитная карта'),
    (3, 'Прямой банковский перевод'),
)

PAYMENT_STATUS = (
    (1, 'В ожидании'),
    (2, 'Ошибка'),
    (3, 'Завершено'),
    (4, 'Отменен'),
    (5, 'Истёк'),
    (6, 'Возвращен'),
)

DELIVERY_STATUS = (
    (1, 'В ожидании'),
    (2, 'На доставке'),
    (3, 'Доставлен'),
    (4, 'Возвращен'),
)


class DeliveryMan(models.Model):
    full_name = models.CharField(max_length=255)
    phone = models.CharField(max_length=10)


class OrderModel(models.Model):
    user = models.ForeignKey('account.UserModel', on_delete=models.RESTRICT, null=True)
    credit_card = models.ForeignKey('paymeuz.Card', on_delete=models.RESTRICT, null=True)
    shipping_address = models.ForeignKey('account.DeliveryAddress', on_delete=models.RESTRICT, null=True, blank=True)
    cart_products = models.ManyToManyField(CartModel)
    price = models.IntegerField(null=True)
    payment_type = models.PositiveSmallIntegerField(choices=PAYMENT_TYPES, default=2)
    payment_status = models.PositiveSmallIntegerField(choices=PAYMENT_STATUS, default=1)
    delivery_status = models.PositiveSmallIntegerField(choices=DELIVERY_STATUS, default=1)
    delivery = models.ForeignKey(DeliveryMan, on_delete=models.RESTRICT, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def get_payme_amount(self):
        return self.price*100


class Advertising(models.Model):
    image = models.ImageField(upload_to=f'medicine/advertising/', null=True, blank=True)
    title = models.CharField(max_length=255)
    text = models.TextField()
    medicine = models.ForeignKey(Product, on_delete=models.RESTRICT, null=True, blank=True)

