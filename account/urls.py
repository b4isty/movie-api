from django.urls import path
from .views import RegisterViewAPI
app_name = 'account'

urlpatterns = [
    path('register', RegisterViewAPI.as_view(), name='register')
]
