from django.urls import path
from .views import (ProductView, CategoryView, GetProductsWithType, GetSingleProduct, CartView,
                    OrderView, AdvertisingView)

urlpatterns = [
    path('category/', CategoryView.as_view()),
    path('category/search/', GetProductsWithType.as_view()),
    path('product/', ProductView.as_view()),
    path('advertising/', AdvertisingView.as_view()),
    path('product/<int:pk>/', GetSingleProduct.as_view()),
    path('cart/', CartView.as_view()),
    path('checkout/', OrderView.as_view()),
]
