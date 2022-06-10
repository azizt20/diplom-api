# Generated by Django 4.0.5 on 2022-06-10 13:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('paymeuz', '0001_initial'),
        ('account', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CartModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.IntegerField(default=1)),
                ('status', models.SmallIntegerField(choices=[(1, 'active'), (2, 'done')], default=1)),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, null=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='category_images')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Category',
                'verbose_name_plural': 'Categories',
            },
        ),
        migrations.CreateModel(
            name='Subcategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('path', models.CharField(max_length=255)),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, null=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='category_images')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('subcategory', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.category')),
            ],
            options={
                'verbose_name': 'Category',
                'verbose_name_plural': 'Categories',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=255, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='product_images')),
                ('price', models.IntegerField(blank=True, null=True)),
                ('sale', models.IntegerField(blank=True, null=True)),
                ('liked', models.BooleanField(default=False)),
                ('in_stock', models.IntegerField(default=0)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.subcategory')),
            ],
            options={
                'verbose_name': 'Product',
                'verbose_name_plural': 'Products',
            },
        ),
        migrations.CreateModel(
            name='OrderModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.IntegerField(null=True)),
                ('payment_type', models.PositiveSmallIntegerField(choices=[(1, 'Оплата при доставке'), (2, 'Кредитная карта'), (3, 'Прямой банковский перевод')], default=2)),
                ('payment_status', models.PositiveSmallIntegerField(choices=[(1, 'В ожидании'), (2, 'Ошибка'), (3, 'Завершено'), (4, 'Отменен'), (5, 'Истёк'), (6, 'Возвращен')], default=1)),
                ('delivery_status', models.PositiveSmallIntegerField(choices=[(1, 'В ожидании'), (2, 'На доставке'), (3, 'Доставлен'), (4, 'Возвращен')], default=1)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('cart_products', models.ManyToManyField(to='shop.cartmodel')),
                ('credit_card', models.ForeignKey(null=True, on_delete=django.db.models.deletion.RESTRICT, to='paymeuz.card')),
                ('shipping_address', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, to='account.deliveryaddress')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.RESTRICT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='cartmodel',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='shop.product'),
        ),
        migrations.AddField(
            model_name='cartmodel',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
    ]
