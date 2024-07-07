import re

from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from .models import User, UserEducation, UserWorkExperience, UserSkill, UserWorkSamples, UserRecommendation, \
    UserLanguage, UserSocialMedia, UserAbout, Partner, ContactUs
from apps.utilities import generate_code


class RegisterSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=50, required=True)
    family = serializers.CharField(max_length=50, required=True)
    user_phone = serializers.CharField(max_length=15, min_length=11, required=True)
    password = serializers.CharField(min_length=6, write_only=True)
    confirm_password = serializers.CharField(min_length=6, write_only=True)
    email = serializers.EmailField(required=True, validators=[
        UniqueValidator(queryset=User.objects.all(), message="ایمیل قبلاً ثبت شده است.")])

    class Meta:
        model = User
        fields = ['name', 'family', 'user_phone', 'password', 'confirm_password', 'email']

    def validate_user_phone(self, value):
        if not re.match(r"^\+?1?\d{11}$", value):
            raise serializers.ValidationError("شماره تلفن باید 11 رقم باشد و فرمت صحیحی داشته باشد.")
        return value

    def validate_password(self, value):
        if len(value) < 6:
            raise serializers.ValidationError("رمز عبور باید حداقل ۶ حرف باشد.")
        if not re.findall('[A-Z]', value):
            raise serializers.ValidationError("رمز عبور باید حداقل یک حرف بزرگ داشته باشد.")
        if not re.findall('[a-z]', value):
            raise serializers.ValidationError("رمز عبور باید حداقل یک حرف کوچک داشته باشد.")
        if not re.findall('[0-9]', value):
            raise serializers.ValidationError("رمز عبور باید حداقل یک عدد داشته باشد.")
        return value

    def validate_email(self, value):
        if not re.match(r"[^@]+@[^@]+\.[^@]+", value):
            raise serializers.ValidationError("ایمیل باید فرمت صحیحی داشته باشد.")
        return value

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError("رمز عبور با تایید آن مطابقت ندارد.")
        return data

    def create(self, validated_data):
        validated_data.pop('confirm_password')
        name = validated_data.pop('name')
        family = validated_data.pop('family')
        user_phone = validated_data.pop('user_phone')
        password = validated_data.pop('password')
        email = validated_data.pop('email')
        active_code = generate_code(5)
        user = User.objects.create_user(user_phone=user_phone, email=email, name=name, family=family, password=password,
                                        active_code=active_code)

        return user


class UserUpdateSerializer(serializers.ModelSerializer):
    age = serializers.IntegerField(required=False)
    gender_class = serializers.ChoiceField(choices=User.GENDER_CHOICES, required=False, allow_blank=True)
    marital_class = serializers.ChoiceField(choices=User.MARITAL_CLASS_CHOICES, required=False, allow_blank=True)
    military_class = serializers.ChoiceField(choices=User.MILITARY_CHOICES, required=False, allow_blank=True)
    birth_date = serializers.DateField(required=False, allow_null=True)
    country = serializers.CharField(required=False, max_length=5000, allow_blank=True)
    city = serializers.CharField(required=False, max_length=5000, allow_blank=True)
    state = serializers.CharField(required=False, max_length=5000, allow_blank=True)
    job = serializers.CharField(required=False, max_length=100, allow_blank=True)
    requested_salary = serializers.IntegerField(required=False, allow_null=True)
    show_salary = serializers.BooleanField(required=False)

    class Meta:
        model = User
        fields = ['age', 'gender_class', 'marital_class', 'military_class',
                  'birth_date', 'country', 'city', 'state', 'job', 'requested_salary', 'show_salary']

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


class ActivateUserSerializer(serializers.Serializer):
    user_phone = serializers.CharField(max_length=15, min_length=11)
    verification_code = serializers.RegexField(
        regex=r'^\d{5}$',
        error_messages={
            'کد نامعتبر': 'کد فعال سازی باید 5 رقم باشد.'
        }
    )

    def validate(self, data):
        user_phone = data.get('user_phone')
        verification_code = data.get('verification_code')

        try:
            user = User.objects.get(user_phone=user_phone)
        except User.DoesNotExist:
            raise serializers.ValidationError("کاربر با این شماره یافت نشد.")
        if user.active_code != verification_code:
            raise serializers.ValidationError("کد نامعتبر است.")

        return data

    def save(self):
        user_phone = self.validated_data['user_phone']
        user = User.objects.get(user_phone=user_phone)
        user.is_active = True
        user.save()
        return user


class UserEducationSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserEducation
        fields = '__all__'
        extra_kwargs = {
            'user': {'read_only': True}
        }

    def create(self, validated_data):
        user = self.context['user']
        return UserEducation.objects.create(user=user, **validated_data)

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


class UserWorkExperienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserWorkExperience
        fields = '__all__'
        extra_kwargs = {
            'user': {'read_only': True}
        }

    def create(self, validated_data):
        user = self.context['user']
        return UserWorkExperience.objects.create(user=user, **validated_data)

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


class UserSkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserSkill
        fields = '__all__'
        extra_kwargs = {
            'user': {'read_only': True}
        }

    def create(self, validated_data):
        user = self.context['user']
        return UserSkill.objects.create(user=user, **validated_data)

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


class UserWorkSamplesSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserWorkSamples
        fields = '__all__'
        extra_kwargs = {
            'user': {'read_only': True}
        }

    def create(self, validated_data):
        user = self.context['user']
        return UserWorkSamples.objects.create(user=user, **validated_data)

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


class UserRecommendationSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserRecommendation
        fields = '__all__'
        extra_kwargs = {
            'user': {'read_only': True}
        }

    def create(self, validated_data):
        user = self.context['user']
        return UserRecommendation.objects.create(user=user, **validated_data)

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


class UserLanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserLanguage
        fields = '__all__'
        extra_kwargs = {
            'user': {'read_only': True}
        }

    def create(self, validated_data):
        user = self.context['user']
        return UserLanguage.objects.create(user=user, **validated_data)

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


class UserSocialMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserSocialMedia
        fields = '__all__'
        extra_kwargs = {
            'user': {'read_only': True}
        }

    def create(self, validated_data):
        user = self.context['user']
        return UserSocialMedia.objects.create(user=user, **validated_data)

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


class UserAboutSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAbout
        fields = '__all__'
        extra_kwargs = {
            'user': {'read_only': True}
        }

    def create(self, validated_data):
        user = self.context['user']
        return UserAbout.objects.create(user=user, **validated_data)

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


class UserPartnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Partner
        fields = '__all__'
        extra_kwargs = {
            'user': {'read_only': True}
        }

    def create(self, validated_data):
        user = self.context['user']
        return Partner.objects.create(user=user, **validated_data)

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


class PartnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Partner
        fields = '__all__'
        extra_kwargs = {
            'user': {'read_only': True}
        }

    def create(self, validated_data):
        user = self.context['user']
        return Partner.objects.create(user=user, **validated_data)

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactUs
        fields = '__all__'

    def create(self, validated_data):
        return ContactUs.objects.create(**validated_data)
