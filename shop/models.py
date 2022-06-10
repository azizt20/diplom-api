from django.db import models


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


class CartModel(models.Model):
    TYPE = (
        (1, 'active'),
        (2, 'done'),
    )
    user = models.ForeignKey('account.UserModel', on_delete=models.SET_NULL, null=True, blank=True)
    product = models.ForeignKey('Product', on_delete=models.RESTRICT)
    amount = models.IntegerField(default=1)
    status = models.SmallIntegerField(default=1, choices=TYPE)

    @property
    def get_total_price(self):
        return self.product.price * self.amount


class OrderModel(models.Model):
    user = models.ForeignKey('account.UserModel', on_delete=models.RESTRICT, null=True)
    credit_card = models.ForeignKey('paymeuz.Card', on_delete=models.RESTRICT, null=True)
    shipping_address = models.ForeignKey('account.DeliveryAddress', on_delete=models.RESTRICT, null=True, blank=True)
    cart_products = models.ManyToManyField(CartModel)
    price = models.IntegerField(null=True)
    payment_type = models.PositiveSmallIntegerField(choices=PAYMENT_TYPES, default=2)
    payment_status = models.PositiveSmallIntegerField(choices=PAYMENT_STATUS, default=1)
    delivery_status = models.PositiveSmallIntegerField(choices=DELIVERY_STATUS, default=1)
    created_at = models.DateTimeField(auto_now_add=True)


class Category(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to='category_images', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        pass

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'


class Subcategory(models.Model):
    subcategory = models.ForeignKey(Category, on_delete=models.CASCADE)
    path = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to='category_images', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        pass

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'


class Product(models.Model):
    product = models.ForeignKey(Subcategory, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='product_images', null=True, blank=True)
    price = models.IntegerField(null=True, blank=True)
    sale = models.IntegerField(null=True, blank=True)
    liked = models.BooleanField(default=False)
    in_stock = models.IntegerField(default=0)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        pass

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'
