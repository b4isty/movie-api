from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny

from .serializers import RegisterSerializer
from .utils import create_jwt_response

User = get_user_model()


class RegisterViewAPI(CreateAPIView):
    """
    API for signup
    """
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny, ]
    queryset = User.objects.all()
    
    def post(self, request, *args, **kwargs):
        resp = super(RegisterViewAPI, self).post(request, *args, **kwargs)
        if resp.status_code == status.HTTP_201_CREATED:
            data = resp.data
            # replace the response data with the jwt dict
            jwt_dict = create_jwt_response(data.get('username'))
            resp.data = jwt_dict
        return resp
