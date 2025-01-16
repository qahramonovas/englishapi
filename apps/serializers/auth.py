from django.contrib.auth.hashers import make_password
from rest_framework.serializers import (
    Serializer, EmailField, CharField)


class UserSerializer(Serializer):
    email = EmailField(max_length=255)
    code = CharField(max_length=5, min_length=5)

class UserRegisterSerializer(Serializer):
    email = EmailField(max_length=255)
    password = CharField(max_length=5, min_length=5)

    def validate_password(self, value):
        return make_password(value)


class EmailSerializer(Serializer):
    email = CharField(max_length=255)