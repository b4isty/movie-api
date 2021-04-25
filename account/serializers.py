from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from rest_framework import serializers

from account.utils import create_jwt_response

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration
    """

    class Meta:
        model = User
        fields = ['username', 'password']
        extra_kwargs = {
            'password': {'write_only': True, 'style': {'input_type': 'password'}},
        }

    def create(self, validated_data):
        # hash the password before storing to the DB
        validated_data['password'] = make_password(validated_data.get('password'))
        user = super(RegisterSerializer, self).create(validated_data)
        return user

