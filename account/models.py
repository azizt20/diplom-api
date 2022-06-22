from django.core.validators import EmailValidator
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from config.validators import PhoneValidator
import datetime

today = datetime.date.today()

class UserManager(BaseUserManager):

    def __create_user(self, username, password, **kwargs):
        username = PhoneValidator.clean(username)
        validator = PhoneValidator()
        validator(username)

        user = UserModel(**kwargs)
        user.username = username
        user.set_password(password)
        user.save()

    def create_user(self, *args, **kwargs):
        kwargs.setdefault('is_staff', False)
        kwargs.setdefault('is_superuser', False)

        if kwargs.get('is_staff') or kwargs.get('is_superuser'):
            raise Exception("User is_staff=False va is_superuser=False bo'lishi shart!")

        return self.__create_user(*args, **kwargs)

    def create_superuser(self, *args, **kwargs):
        kwargs.setdefault('is_staff', True)
        kwargs.setdefault('is_superuser', True)

        if not kwargs.get('is_staff') or not kwargs.get('is_superuser'):
            raise Exception("User is_staff=True va is_superuser=True bo'lishi shart!")

        return self.__create_user(*args, **kwargs)


class UserModel(AbstractUser):
    objects = UserManager()
    username = models.CharField(max_length=15, unique=True,
                                validators=[PhoneValidator()], help_text="Пожалуйста, укажите свой пароль")
    password = models.CharField(max_length=256, null=True, blank=True)
    email = models.EmailField(validators=[EmailValidator()], null=True, blank=True)
    avatar = models.ImageField(upload_to=f'avatars/{today.year}-{today.month}-{today.month}/', null=True, blank=True)
    address = models.ForeignKey('RegionModel', on_delete=models.RESTRICT, null=True, blank=True)
    language = models.CharField(max_length=3, null=True, blank=True)

    username_validator = PhoneValidator()

    class Meta:
        verbose_name = "user"
        verbose_name_plural = "users"

    def __str__(self):
        return self.username


# Sms kode
class SmsCode(models.Model):
    phone = models.CharField(max_length=16, db_index=True)
    ip = models.GenericIPAddressField(db_index=True)
    code = models.CharField(max_length=10)
    expire_at = models.DateTimeField(db_index=True)

    class Meta:
        index_together = []


# Sms try
class SmsAttempt(models.Model):
    phone = models.CharField(max_length=16, db_index=True)
    counter = models.IntegerField(default=0)
    last_attempt_at = models.DateTimeField(db_index=True)


class RegionModel(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class CityModel(models.Model):
    region = models.ForeignKey(RegionModel, on_delete=models.RESTRICT, null=True, blank=True)
    name = models.CharField(max_length=100)
    delivery_price = models.IntegerField(default=0, null=True)

    def __str__(self):
        return self.name


class DeliveryAddress(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.RESTRICT)
    name = models.CharField(max_length=255, null=True, blank=True)
    city = models.ForeignKey(CityModel, on_delete=models.RESTRICT, null=True)
    full_address = models.CharField(max_length=255, null=True, blank=True)
    postcode = models.CharField(max_length=255, null=True, blank=True)
    door_or_phone = models.CharField(max_length=255, null=True, blank=True)
    instructions = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.name
