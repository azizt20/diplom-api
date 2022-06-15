from django.urls import path
from .views import (MedicinesView, TypeMedicineView, GetMedicinesWithType, GetSingleMedicine, CartView,
                    OrderView, AdvertisingView)

urlpatterns = [
    path('types/', TypeMedicineView.as_view()),
    path('types/search/', GetMedicinesWithType.as_view()),
    path('product/', MedicinesView.as_view()),
    path('advertising/', AdvertisingView.as_view()),
    path('product/<int:pk>/', GetSingleMedicine.as_view()),
    path('cart/', CartView.as_view()),
    path('checkout/', OrderView.as_view()),
]
