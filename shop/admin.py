from django.contrib import admin
# from modeltranslation.admin import TabbedTranslationAdmin
from .models import Product, Category, OrderModel, CartModel, Pictures,DeliveryMan


# class TypeMedicineAdmin(TabbedTranslationAdmin):
#     list_display = ('id', 'name',)
#
#
# class MedicineAdmin(TabbedTranslationAdmin):
#     list_display = ('id', 'name', 'title', )


admin.site.register(Product)
admin.site.register(Category)
admin.site.register(OrderModel)
admin.site.register(CartModel)
admin.site.register(Pictures)
admin.site.register(DeliveryMan)

# Register your models here.
