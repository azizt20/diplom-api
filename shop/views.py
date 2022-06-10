from django.shortcuts import render
from .models import Product, Subcategory, Category
from .serializers import ProductSerializer, CategorySerializer, SubcategorySerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated


class CategoryView(APIView):

    permission_classes = (IsAuthenticated,)

    def get(self, request):
        categories = Category.objects.all()
        serializers = CategorySerializer(categories, many=True)

        return Response({
            'status': 'success',
            'data': serializers.data
        })


class SubcategoryView(APIView):

    permission_classes = (IsAuthenticated,)

    def get(self, request):
        categories = Subcategory.objects.all()
        serializers = SubcategorySerializer(categories, many=True)

        return Response({
            'status': 'success',
            'data': serializers.data
        })


class ProductView(APIView):

    permission_classes = (IsAuthenticated,)

    def get(self, request):
        products = Product.objects.all()
        serializers = ProductSerializer(products, many=True)

        return Response({
            'status': 'success',
            'data': serializers.data
        })


