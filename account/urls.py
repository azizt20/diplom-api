from django.urls import path
from .views import (SendSmsView, ConfirmSmsView, RegistrationView, CityView, RegionView, AddAddressView,
                    UserView, DeliverAddressView)
urlpatterns = [
    path('send/sms/', SendSmsView.as_view()),
    path('send/sms/confirm/', ConfirmSmsView.as_view()),
    path('registration/', RegistrationView.as_view()),
    path('region/', RegionView.as_view()),
    path('city/', CityView.as_view()),
    path('add/address/<int:pk>/', AddAddressView.as_view()),
    path('me/', UserView.as_view()),
    path('deliver/address/', DeliverAddressView.as_view()),

]


