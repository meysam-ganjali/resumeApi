from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from apps.permission import CheckPermission
from apps.utilities import response_formatter

from apps.accounts.serializer import UserUpdateSerializer, RegisterSerializer, ActivateUserSerializer


class RegisterAPIView(APIView):
    @extend_schema(
        request=RegisterSerializer,
        responses={200},
    )
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            res = serializer.save()
            return Response(response_formatter({
                'active_code': res.active_code,
                'phone': res.user_phone
            }, status.HTTP_201_CREATED,
                'حساب کاربری با موفقیت ایجاد شد. برای ادامه موبایل خود را تایید کنید.'))
        return Response(response_formatter(serializer.errors, status.HTTP_400_BAD_REQUEST, 'خطاهای اعتبارسنجی'))


class UserUpdateApiView(APIView):
    @extend_schema(
        request=UserUpdateSerializer,
        responses={200},
    )
    def put(self, request, *args, **kwargs):
        permission_classes = [IsAuthenticated, CheckPermission]
        authentication_classes = JWTAuthentication
        user = request.user
        serializer = UserUpdateSerializer(user, data=request.data, partial=True)
        if user and user.is_authenticated:
            if serializer.is_valid():
                serializer.save()
                return Response(response_formatter(None, status.HTTP_200_OK, 'به مرحله بعد بروید.'))
            else:
                return Response(
                    response_formatter(serializer.errors, status.HTTP_400_BAD_REQUEST, 'خطاهای اعتبار سنجی.'))
        return Response(response_formatter(None, status.HTTP_403_FORBIDDEN,
                                           'مجوز برای این بخش صادر نشد.ابتدا وارد حساب کاربری خود شوید.'))


class ActivateUserApiView(APIView):
    @extend_schema(
        request=ActivateUserSerializer,
        responses={200}
    )
    def post(self, request):
        serializer = ActivateUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(response_formatter({}, status.HTTP_200_OK, 'حساب شما با موفقیت فعال شد'))
        return Response(response_formatter(serializer.errors, status.HTTP_400_BAD_REQUEST, 'خطاهای اعتبارسنجی'))
