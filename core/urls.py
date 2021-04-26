from django.urls import path
from .views import RequestCounterRetrieveAPIView, RequestCounterResetAPIView

app_name = 'core'

urlpatterns = [
    path('', RequestCounterRetrieveAPIView.as_view(), name='request-count'),
    path('reset/', RequestCounterResetAPIView.as_view(), name='request-reset')
]