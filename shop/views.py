from django.conf import settings
from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from .filters import ProductFilter
from account.models import DeliveryAddress
from config.responses import ResponseSuccess, ResponseFail
from .serializers import (CategorySerializer, ProductSerializer, CartSerializer, OrderCreateSerializer,
                          OrderShowSerializer, AdvertisingSerializer)
from .models import Pictures, Category, Product, CartModel, OrderModel, Advertising
from paymeuz.models import Card


class AdvertisingView(APIView):
    # permission_classes = (IsAuthenticated,)

    def get(self, request):
        types = Advertising.objects.all()
        serializer = AdvertisingSerializer(types, many=True)
        return ResponseSuccess(data=serializer.data, request=request.method)


class CategoryView(APIView):
    # permission_classes = (IsAuthenticated,)

    def get(self, request):
        types = Category.objects.all()
        serializer = CategorySerializer(types, many=True)
        return ResponseSuccess(data=serializer.data, request=request.method)


class ProductView(APIView):
    # permission_classes = (IsAuthenticated,)

    def get(self, request):
        products = Product.objects.all()
        q = ProductFilter(request.GET, queryset=products).qs
        serializer = ProductSerializer(q, many=True)
        return ResponseSuccess(data=serializer.data, request=request.method)

    def post(self, request):
        key = request.data['key']
        medicine = Product.objects.filter(name__contains=key)
        serializer = ProductSerializer(medicine, many=True)
        return ResponseSuccess(data=serializer.data, request=request.method)


class GetProductsWithType(APIView):
    # permission_classes = (IsAuthenticated,)

    def post(self, request):
        id_list = list(request.data['list'].split(','))
        medicine = Product.objects.filter(type_medicine_id__in=id_list)
        serializer = ProductSerializer(medicine, many=True)
        return ResponseSuccess(data=serializer.data, request=request.method)


class GetSingleProduct(APIView):
    # permission_classes = (IsAuthenticated,)

    def get(self, request, pk):
        medicine = Product.objects.get(id=pk)
        serializer = ProductSerializer(medicine)
        return ResponseSuccess(data=serializer.data, request=request.method)


class CartView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        carts = CartModel.objects.filter(user=request.user, status=1)
        serializer = CartSerializer(carts, many=True)
        return ResponseSuccess(data=serializer.data, request=request.method)

    def post(self, request):
        serializer = CartSerializer(data=request.data, context={'request': request})
        med = Product.objects.get(id=request.data['product'])
        if serializer.is_valid():
            cart = CartModel.objects.create(user=request.user, product=med)
            # serializer.save()
            serializer = CartSerializer(cart)
            return ResponseSuccess(data=serializer.data, request=request.method)
        else:
            return ResponseFail(data=serializer.errors, request=request.method)

    def put(self, request):
        cart = CartModel.objects.get(id=request.data['id'], user=request.user)
        serializer = CartSerializer(instance=cart, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return ResponseSuccess(data=serializer.data, request=request.method)
        else:
            return ResponseFail(data=serializer.errors, request=request.method)

    def delete(self, request):
        try:
            CartModel.objects.get(id=request.GET['id'], user=request.user).delete()
            return ResponseSuccess(request=request.method)
        except:
            return ResponseFail(request=request.method)


class OrderView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        orders = OrderModel.objects.filter(user=request.user)
        serializer = OrderShowSerializer(orders, many=True)
        return ResponseSuccess(data=serializer.data, request=request.method)

    def put(self, request):
        card_id = request.data['card_id']
        order_id = request.data['order_id']
        o = OrderModel.objects.get(id=order_id)
        o.credit_card = Card.objects.get(id=card_id)
        o.save()
        return ResponseSuccess(request=request.method)

    def post(self, request):
        carts = CartModel.objects.filter(user=request.user, status=1)
        order = OrderModel()
        order.user = request.user
        order.save()
        summa = 0
        for i in carts:
            order.cart_products.add(i)
            summa += i.get_total_price
            i.status = 2
            i.save()
        order.price = summa
        order.save()
        serializer = OrderShowSerializer(order)
        return ResponseSuccess(data=serializer.data, request=request.method)

    def put(self, request):
        try:
            order = OrderModel.objects.get(id=request.data['id'])
        except:
            return ResponseFail(data='Order not found')
        try:
            id = request.data['shipping_address']
            da = DeliveryAddress.objects.get(id=id)
            add_key = 1
        except:
            add_key = 0
        del request.data['id']
        serializer = OrderCreateSerializer(order, data=request.data)
        if serializer.is_valid():
            if add_key == 1:
                if order.shipping_address is None:
                    if da.city.delivery_price == 0:
                        order.price = order.price + settings.DEFAULT_DELIVERY_COST
                    else:
                        order.price = order.price + da.city.delivery_price
                else:
                    old_price = order.shipping_address.city.delivery_price
                    print(old_price)
                    if old_price == 0:
                        order.price = order.price - settings.DEFAULT_DELIVERY_COST
                        print('1')
                    else:
                        order.price = order.price - old_price
                    if da.city.delivery_price == 0:
                        order.price = order.price + settings.DEFAULT_DELIVERY_COST
                    else:
                        order.price = order.price + da.city.delivery_price
            order.save()
            serializer.save()
            serializer = OrderShowSerializer(order)
            return ResponseSuccess(data=serializer.data, request=request.method)
        else:
            return ResponseFail(data=serializer.errors, request=request.method)
