from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from apps.accounts.models import UserEducation, UserWorkExperience, UserSkill, UserWorkSamples, UserRecommendation, \
    UserLanguage, UserSocialMedia
from apps.permission import CheckPermission
from apps.utilities import response_formatter

from apps.accounts.serializer import UserUpdateSerializer, RegisterSerializer, ActivateUserSerializer, \
    UserEducationSerializer, UserWorkExperienceSerializer, UserSkillSerializer, UserWorkSamplesSerializer, \
    UserRecommendationSerializer, UserLanguageSerializer, UserSocialMediaSerializer


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


class AddUserEducationView(APIView):
    @extend_schema(
        request=UserEducationSerializer,
        responses={200}
    )
    def post(self, request):
        permission_classes = [IsAuthenticated, CheckPermission]
        authentication_classes = JWTAuthentication
        user = request.user
        if user and user.is_authenticated:
            serializer = UserEducationSerializer(data=request.data, context={'user': user})
            if serializer.is_valid():
                serializer.save()
                return Response(response_formatter(serializer.data, status.HTTP_200_OK, 'مقطع تحصیلی ایجاد شد.'))
            return Response(response_formatter(serializer.errors, status.HTTP_400_BAD_REQUEST, 'خطاهای اعتبارسنجی'))
        return Response(response_formatter(None, status.HTTP_403_FORBIDDEN, 'لطفا وارد حساب کاربری خود شوید.'))


class UpdateUserEducationView(APIView):
    @extend_schema(
        request=UserEducationSerializer,
        responses={200}
    )
    def put(self, request, pk):
        permission_classes = [IsAuthenticated, CheckPermission]
        authentication_classes = JWTAuthentication
        user = request.user
        if user and user.is_authenticated:
            try:
                instance = UserEducation.objects.get(pk=pk)
            except UserEducation.DoesNotExist:
                return Response(response_formatter(None, status.HTTP_404_NOT_FOUND, 'مقطع تحصیلی یافت نشد.'))

            serializer = UserEducationSerializer(instance, data=request.data, context={'user': user})
            if serializer.is_valid():
                serializer.save()
                return Response(response_formatter(serializer.data, status.HTTP_200_OK, 'مقطع تحصیلی بروزشد.'))
            return Response(response_formatter(serializer.errors, status.HTTP_400_BAD_REQUEST, 'خطاهای اعتبارسنجی'))
        return Response(response_formatter(None, status.HTTP_403_FORBIDDEN, 'لطفا وارد حساب کاربری خود شوید.'))


class AddUserWorkExperience(APIView):
    @extend_schema(
        request=UserWorkExperienceSerializer,
        responses={200}
    )
    def post(self, request):
        permission_classes = [IsAuthenticated, CheckPermission]
        authentication_classes = JWTAuthentication
        user = request.user
        if user and user.is_authenticated:
            serializer = UserWorkExperienceSerializer(data=request.data, context={'user': user})
            if serializer.is_valid():
                serializer.save()
                return Response(response_formatter(serializer.data, status.HTTP_200_OK, 'سابقه کار ایجاد شد.'))
            return Response(response_formatter(serializer.errors, status.HTTP_400_BAD_REQUEST, 'خطاهای اعتبارسنجی'))
        return Response(response_formatter(None, status.HTTP_403_FORBIDDEN, 'لطفا وارد حساب کاربری خود شوید.'))


class UpdateUserWorkExperience(APIView):
    @extend_schema(
        request=UserWorkExperienceSerializer,
        responses={200}
    )
    def put(self, request, pk):
        permission_classes = [IsAuthenticated, CheckPermission]
        authentication_classes = JWTAuthentication
        user = request.user
        if user and user.is_authenticated:
            try:
                instance = UserWorkExperience.objects.get(pk=pk)
            except UserEducation.DoesNotExist:
                return Response(response_formatter(None, status.HTTP_404_NOT_FOUND, 'سابقه کار یافت نشد.'))

            serializer = UserWorkExperienceSerializer(instance, data=request.data, context={'user': user})
            if serializer.is_valid():
                serializer.save()
                return Response(response_formatter(serializer.data, status.HTTP_200_OK, 'سابقه کار بروزشد.'))
            return Response(response_formatter(serializer.errors, status.HTTP_400_BAD_REQUEST, 'خطاهای اعتبارسنجی'))
        return Response(response_formatter(None, status.HTTP_403_FORBIDDEN, 'لطفا وارد حساب کاربری خود شوید.'))


class AddUserSkillApiView(APIView):
    @extend_schema(
        description="skill_type:('H', 'سخت'), ('S', 'نرم')",
        request=UserSkillSerializer,
        responses={200}
    )
    def post(self, request):
        permission_classes = [IsAuthenticated, CheckPermission]
        authentication_classes = JWTAuthentication
        user = request.user
        if user and user.is_authenticated:
            serializer = UserSkillSerializer(data=request.data, context={'user': user})
            if serializer.is_valid():
                serializer.save()
                return Response(response_formatter(serializer.data, status.HTTP_200_OK, 'مهارت ایجاد شد.'))
            return Response(response_formatter(serializer.errors, status.HTTP_400_BAD_REQUEST, 'خطاهای اعتبارسنجی'))
        return Response(response_formatter(None, status.HTTP_403_FORBIDDEN, 'لطفا وارد حساب کاربری خود شوید.'))


class UpdateUserSkillApiView(APIView):
    @extend_schema(
        description="skill_type:('H', 'سخت'), ('S', 'نرم')",
        request=UserSkillSerializer,
        responses={200}
    )
    def put(self, request, pk):
        permission_classes = [IsAuthenticated, CheckPermission]
        authentication_classes = JWTAuthentication
        user = request.user
        if user and user.is_authenticated:
            try:
                instance = UserSkill.objects.get(pk=pk)
            except UserEducation.DoesNotExist:
                return Response(response_formatter(None, status.HTTP_404_NOT_FOUND, 'مهارت یافت نشد.'))

            serializer = UserSkillSerializer(instance, data=request.data, context={'user': user})
            if serializer.is_valid():
                serializer.save()
                return Response(response_formatter(serializer.data, status.HTTP_200_OK, 'مهارت بروزشد.'))
            return Response(response_formatter(serializer.errors, status.HTTP_400_BAD_REQUEST, 'خطاهای اعتبارسنجی'))
        return Response(response_formatter(None, status.HTTP_403_FORBIDDEN, 'لطفا وارد حساب کاربری خود شوید.'))


class AddUserWorkSamplesApiView(APIView):
    @extend_schema(
        request=UserWorkSamplesSerializer,
        responses={200}
    )
    def post(self, request):
        permission_classes = [IsAuthenticated, CheckPermission]
        authentication_classes = JWTAuthentication
        user = request.user
        if user and user.is_authenticated:
            serializer = UserWorkSamplesSerializer(data=request.data, context={'user': user})
            if serializer.is_valid():
                serializer.save()
                return Response(response_formatter(serializer.data, status.HTTP_200_OK, 'نمونه کار ایجاد شد.'))
            return Response(response_formatter(serializer.errors, status.HTTP_400_BAD_REQUEST, 'خطاهای اعتبارسنجی'))
        return Response(response_formatter(None, status.HTTP_403_FORBIDDEN, 'لطفا وارد حساب کاربری خود شوید.'))


class UpdateUserWorkSamplesApiView(APIView):
    @extend_schema(
        request=UserWorkSamplesSerializer,
        responses={200}
    )
    def put(self, request, pk):
        permission_classes = [IsAuthenticated, CheckPermission]
        authentication_classes = JWTAuthentication
        user = request.user
        if user and user.is_authenticated:
            try:
                instance = UserWorkSamples.objects.get(pk=pk)
            except UserEducation.DoesNotExist:
                return Response(response_formatter(None, status.HTTP_404_NOT_FOUND, 'نمونه کار یافت نشد.'))
            serializer = UserWorkSamplesSerializer(instance, data=request.data, context={'user': user})
            if serializer.is_valid():
                serializer.save()
                return Response(response_formatter(serializer.data, status.HTTP_200_OK, 'نمونه کار بروزشد.'))
            return Response(response_formatter(serializer.errors, status.HTTP_400_BAD_REQUEST, 'خطاهای اعتبارسنجی'))
        return Response(response_formatter(None, status.HTTP_403_FORBIDDEN, 'لطفا وارد حساب کاربری خود شوید.'))


class AddUserRecommendationApiView(APIView):
    @extend_schema(
        request=UserRecommendationSerializer,
        responses={200}
    )
    def post(self, request):
        permission_classes = [IsAuthenticated, CheckPermission]
        authentication_classes = JWTAuthentication
        user = request.user
        if user and user.is_authenticated:
            serializer = UserRecommendationSerializer(data=request.data, context={'user': user})
            if serializer.is_valid():
                serializer.save()
                return Response(response_formatter(serializer.data, status.HTTP_200_OK, 'توصیه نامه ایجاد شد.'))
            return Response(response_formatter(serializer.errors, status.HTTP_400_BAD_REQUEST, 'خطاهای اعتبارسنجی'))
        return Response(response_formatter(None, status.HTTP_403_FORBIDDEN, 'لطفا وارد حساب کاربری خود شوید.'))


class UpdateUserRecommendationApiView(APIView):
    @extend_schema(
        request=UserRecommendationSerializer,
        responses={200}
    )
    def put(self, request, pk):
        permission_classes = [IsAuthenticated, CheckPermission]
        authentication_classes = JWTAuthentication
        user = request.user
        if user and user.is_authenticated:
            try:
                instance = UserRecommendation.objects.get(pk=pk)
            except UserEducation.DoesNotExist:
                return Response(response_formatter(None, status.HTTP_404_NOT_FOUND, 'توصیه نامه یافت نشد.'))
            serializer = UserRecommendationSerializer(instance, data=request.data, context={'user': user})
            if serializer.is_valid():
                serializer.save()
                return Response(response_formatter(serializer.data, status.HTTP_200_OK, 'توصیه نامه بروزشد.'))
            return Response(response_formatter(serializer.errors, status.HTTP_400_BAD_REQUEST, 'خطاهای اعتبارسنجی'))
        return Response(response_formatter(None, status.HTTP_403_FORBIDDEN, 'لطفا وارد حساب کاربری خود شوید.'))


class AddUserLanguageApiView(APIView):
    @extend_schema(
        request=UserLanguageSerializer,
        responses={200}
    )
    def post(self, request):
        permission_classes = [IsAuthenticated, CheckPermission]
        authentication_classes = JWTAuthentication
        user = request.user
        if user and user.is_authenticated:
            serializer = UserLanguageSerializer(data=request.data, context={'user': user})
            if serializer.is_valid():
                serializer.save()
                return Response(response_formatter(serializer.data, status.HTTP_200_OK, 'مهارت زبان ایجاد شد.'))
            return Response(response_formatter(serializer.errors, status.HTTP_400_BAD_REQUEST, 'خطاهای اعتبارسنجی'))
        return Response(response_formatter(None, status.HTTP_403_FORBIDDEN, 'لطفا وارد حساب کاربری خود شوید.'))


class UpdateUserLanguageApiView(APIView):
    @extend_schema(
        request=UserLanguageSerializer,
        responses={200}
    )
    def put(self, request, pk):
        permission_classes = [IsAuthenticated, CheckPermission]
        authentication_classes = JWTAuthentication
        user = request.user
        if user and user.is_authenticated:
            try:
                instance = UserLanguage.objects.get(pk=pk)
            except UserEducation.DoesNotExist:
                return Response(response_formatter(None, status.HTTP_404_NOT_FOUND, 'مهارت زبان یافت نشد.'))
            serializer = UserLanguageSerializer(instance, data=request.data, context={'user': user})
            if serializer.is_valid():
                serializer.save()
                return Response(response_formatter(serializer.data, status.HTTP_200_OK, 'مهارت بروزشد.'))
            return Response(response_formatter(serializer.errors, status.HTTP_400_BAD_REQUEST, 'خطاهای اعتبارسنجی'))
        return Response(response_formatter(None, status.HTTP_403_FORBIDDEN, 'لطفا وارد حساب کاربری خود شوید.'))


class AddUserSocialMediaApiView(APIView):
    @extend_schema(
        request=UserSocialMediaSerializer,
        responses={200}
    )
    def post(self, request):
        permission_classes = [IsAuthenticated, CheckPermission]
        authentication_classes = JWTAuthentication
        user = request.user
        if user and user.is_authenticated:
            serializer = UserSocialMediaSerializer(data=request.data, context={'user': user})
            if serializer.is_valid():
                serializer.save()
                return Response(response_formatter(serializer.data, status.HTTP_200_OK, 'شبکه اجتماعی ایجاد شد.'))
            return Response(response_formatter(serializer.errors, status.HTTP_400_BAD_REQUEST, 'خطاهای اعتبارسنجی'))
        return Response(response_formatter(None, status.HTTP_403_FORBIDDEN, 'لطفا وارد حساب کاربری خود شوید.'))


class UpdateUserSocialMediaApiView(APIView):
    @extend_schema(
        request=UserLanguageSerializer,
        responses={200}
    )
    def put(self, request, pk):
        permission_classes = [IsAuthenticated, CheckPermission]
        authentication_classes = JWTAuthentication
        user = request.user
        if user and user.is_authenticated:
            try:
                instance = UserSocialMedia.objects.get(pk=pk)
            except UserEducation.DoesNotExist:
                return Response(response_formatter(None, status.HTTP_404_NOT_FOUND, 'شبکه اجتماعی یافت نشد.'))
            serializer = UserSocialMediaSerializer(instance, data=request.data, context={'user': user})
            if serializer.is_valid():
                serializer.save()
                return Response(response_formatter(serializer.data, status.HTTP_200_OK, 'شبکه اجتماعی بروزشد.'))
            return Response(response_formatter(serializer.errors, status.HTTP_400_BAD_REQUEST, 'خطاهای اعتبارسنجی'))
        return Response(response_formatter(None, status.HTTP_403_FORBIDDEN, 'لطفا وارد حساب کاربری خود شوید.'))
