from django.contrib import admin
# from modeltranslation.admin import TabbedTranslationAdmin
from .models import Product, TypeProduct, OrderModel, CartModel, PicturesMedicine


# class TypeMedicineAdmin(TabbedTranslationAdmin):
#     list_display = ('id', 'name',)
#
#
# class MedicineAdmin(TabbedTranslationAdmin):
#     list_display = ('id', 'name', 'title', )


admin.site.register(Product)
admin.site.register(TypeProduct)
admin.site.register(OrderModel)
admin.site.register(CartModel)
admin.site.register(PicturesMedicine)

# Register your models here.
