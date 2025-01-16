import random
from datetime import timedelta
from http import HTTPStatus

import redis
from drf_spectacular.utils import extend_schema
from rest_framework.exceptions import ValidationError
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from apps.models import User
from apps.serializers import EmailSerializer, UserSerializer, UserRegisterSerializer
from apps.tasks import send_email_task


@extend_schema(tags=['auth'])
class CustomTokenObtainPairView(TokenObtainPairView):
    pass

@extend_schema(tags=['auth'])
class CustomTokenRefreshView(TokenRefreshView):
    pass

@extend_schema(
    request=EmailSerializer,
    tags=['auth'])
class SendEmailAPIView(APIView):
    def post(self , request):
        email = request.data.get('email')
        query = User.objects.filter(email=email)
        if not query.exists():
            User.objects.create(email=email, is_active=False)
        elif query.first().is_active:
            raise ValidationError("Bunday email mavjud!" , HTTPStatus.BAD_REQUEST)

        code = str(random.randrange(10**4,10**5))
        send_email_task.delay(email=email ,code=code)
        r = redis.Redis()
        r.mset({email : code})
        r.expire(email , time=timedelta(minutes=5))
        return Response({"message" : "Success"} , status=HTTPStatus.OK)


@extend_schema(tags=['auth'])
class CodeUserAPIView(APIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        code = request.data.get('code')
        r = redis.Redis(decode_responses=True)
        verify_code = r.mget(email)[0]
        if verify_code != code:
            raise ValidationError("Not Match Code" , HTTPStatus.BAD_REQUEST)
        User.objects.filter(email = email).update(is_active=True)
        return Response({"message" : True} , HTTPStatus.OK)

@extend_schema(tags=['auth'])
class RegisterUserCreateAPIView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        email = data.get('email')
        password = data.get('password')
        query = User.objects.filter(email = email)
        if not query.exists():
            raise ValidationError("Tastiqlanmagan email kiritildi!", HTTPStatus.BAD_REQUEST)
        elif not query.first().is_active:
            raise ValidationError("Tastiqlanmagan email kiritildi!", HTTPStatus.BAD_REQUEST)
        else:
            query.update(password=password)
        return Response({'response' : "Success register"} , HTTPStatus.CREATED)













