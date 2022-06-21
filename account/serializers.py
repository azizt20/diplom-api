from rest_framework import serializers
from .models import UserModel, RegionModel, CityModel, DeliveryAddress
from config.validators import PhoneValidator


class SmsSerializer(serializers.Serializer):
    phone = serializers.CharField(validators=[PhoneValidator()])


class ConfirmSmsSerializer(serializers.Serializer):
    phone = serializers.CharField(validators=[PhoneValidator()])
    code = serializers.CharField(min_length=6, max_length=6)


class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ['first_name', 'last_name', 'password', 'avatar']
        extra_kwargs = {
            'password': {'write_only': True},
            'avatar': {'required': False},
        }

    def update(self, instance, validated_data):
        print('laaaaaaaaaaaa')
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance


class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegionModel
        fields = '__all__'


class CitySerializer(serializers.ModelSerializer):
    # country = RegionSerializer()

    class Meta:
        model = CityModel
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserModel
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'avatar']
        extra_kwargs = {
            'username': {'read_only': True},
            'first_name': {'required': False},
            'last_name': {'required': False},
            'email': {'required': False},
            'avatar': {'required': False},
        }


class DeliverAddressSerializer(serializers.ModelSerializer):

    class Meta:
        model = DeliveryAddress
        fields = ['id', 'name', 'region', 'full_address', 'apartment_office', 'floor', 'door_or_phone', 'instructions']
        extra_kwargs = {
            'id': {'read_only': True},
            'name': {'required': False},
            'region': {'required': False},
            'full_address': {'required': False},
            'apartment_office': {'required': False},
            'floor': {'required': False},
            'door_or_phone': {'required': False},
            'instructions': {'required': False},
        }



