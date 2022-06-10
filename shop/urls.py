from django.urls import path
from .views import CategoryView, ProductView, SubcategoryView


urlpatterns = [
    path('category/', CategoryView.as_view()),
    path('subcategory/', SubcategoryView.as_view()),
    path('product/', ProductView.as_view()),
]
