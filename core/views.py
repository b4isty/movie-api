from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import DestroyModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from core.models import RequestCounter
from core.renderers import RequestCounterJSONRenderer
from core.serializers import RequestCounterSerializer


class RequestCounterRetrieveAPIView(GenericAPIView):
    """Request Counter API View returns the request count served till now"""
    serializer_class = RequestCounterSerializer
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        qs = RequestCounter.objects.all()
        return qs

    def get(self, request, *args, **kwargs):
        obj = self.get_object()
        serializer = self.serializer_class(obj)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def get_object(self):
        return RequestCounter.objects.first()


class RequestCounterResetAPIView(GenericAPIView):
    """ Request Counter API View rest the request count"""
    serializer_class = RequestCounterSerializer
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = RequestCounter.objects.all()

    def post(self, request, *args, **kwargs):
        self.filter_queryset(self.get_queryset()).update(count=0)
        return Response(data={"message": "request count reset successfully"}, status=status.HTTP_200_OK)
