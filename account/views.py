from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from .models import UserModel, RegionModel, CityModel, DeliveryAddress
from config.helpers import send_sms_code, validate_sms_code
from config.responses import ResponseFail, ResponseSuccess
from .serializers import (SmsSerializer, ConfirmSmsSerializer, RegistrationSerializer,
                          RegionSerializer, CitySerializer, UserSerializer, DeliverAddressSerializer)


class SendSmsView(APIView):
    def get(self, request):
        serializer = SmsSerializer()
        return ResponseSuccess(data=serializer.data, request=request.method)

    def post(self, request):
        serializer = SmsSerializer(data=request.data)
        if serializer.is_valid():
            send_sms_code(request, serializer.data['phone'])
            return ResponseSuccess(request=request.method)
        return ResponseFail(data=serializer.errors, request=request.method)


class ConfirmSmsView(APIView):

    def get(self, request):
        serializer = ConfirmSmsSerializer()
        return ResponseSuccess(data=serializer.data, request=request.method)

    def post(self, request):
        serializer = ConfirmSmsSerializer(data=request.data)
        if serializer.is_valid():
            if validate_sms_code(serializer.data['phone'], serializer.data['code']):
                return ResponseSuccess(data="Telefon nomer tasdiqladi", request=request.method)
            else:
                return ResponseFail(data='Code hato kiritilgan', request=request.method)
        return ResponseFail(data=serializer.errors, request=request.method)


class RegistrationView(APIView):

    def get(self, request):
        serializer = RegistrationSerializer()
        return ResponseSuccess(data=serializer.data, request=request.method)

    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return ResponseSuccess(data=serializer.data, request=request.method)
        else:
            return ResponseFail(data=serializer.errors, request=request.method)


class UserView(APIView):
    queryset = UserModel.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user = UserModel.objects.get(id=request.user.id)
        serializer = UserSerializer(user)
        return ResponseSuccess(data=serializer.data, request=request.method)

    def put(self, request):
        serializer = UserSerializer(request.user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return ResponseSuccess(data=serializer.data, request=request.method)
        else:
            return ResponseFail(data=serializer.errors, request=request.method)


class CityView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        reg = CityModel.objects.all()
        serializer = CitySerializer(reg, many=True)
        return ResponseSuccess(data=serializer.data, request=request.method)


class RegionView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        coun = RegionModel.objects.all()
        serializer = RegionSerializer(coun, many=True)
        return ResponseSuccess(data=serializer.data, request=request.method)


class AddAddressView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, pk):
        try:
            city = CityModel.objects.get(id=pk)
        except:
            return ResponseFail(data='Bunday Viloyat mavjud emas', request=request.method)
        user = request.user
        user.address = city
        user.save()
        return ResponseSuccess(request=request.method)


class DeliverAddressView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        address = DeliveryAddress.objects.filter(user=request.user)
        serializers = DeliverAddressSerializer(address, many=True)
        return ResponseSuccess(data=serializers.data, request=request.method)

    def post(self, request):
        city = CityModel.objects.get(id=request.data["city"])
        serializers = DeliverAddressSerializer(data=request.data)
        del request.data["city"]
        if serializers.is_valid():
            da = DeliveryAddress(**serializers.data)
            da.user = request.user
            da.city = city
            da.save()
            return ResponseSuccess(data=serializers.data, request=request.method)
        else:
            return ResponseFail(data=serializers.errors, request=request.method)

