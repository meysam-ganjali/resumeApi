from django.contrib import admin
from easy_select2 import select2_modelform

from .models import (User, UserEducation, UserWorkExperience, UserSkill, UserWorkSamples, UserRecommendation,
                     UserLanguage, UserSocialMedia, UserAbout, ContactUs, Partner)

UserForm = select2_modelform(User, attrs={'width': '150px'})
UserEducationForm = select2_modelform(UserEducation, attrs={'width': '150px'})
UserWorkExperienceForm = select2_modelform(UserWorkExperience, attrs={'width': '150px'})
UserSkillForm = select2_modelform(UserSkill, attrs={'width': '150px'})
UserWorkSamplesForm = select2_modelform(UserWorkSamples, attrs={'width': '150px'})
UserRecommendationForm = select2_modelform(UserRecommendation, attrs={'width': '150px'})
UserLanguageForm = select2_modelform(UserLanguage, attrs={'width': '150px'})
UserSocialMediaForm = select2_modelform(UserSocialMedia, attrs={'width': '150px'})
UserAboutForm = select2_modelform(UserAbout, attrs={'width': '150px'})


class UserEducationInstanceAdminInline(admin.TabularInline):
    model = UserEducation
    extra = 2
    form = UserEducationForm


class UserWorkExperienceInstanceAdminInline(admin.StackedInline):
    model = UserWorkExperience
    extra = 2
    form = UserWorkExperienceForm


class UserSkillInstanceAdminInline(admin.TabularInline):
    model = UserSkill
    extra = 4
    form = UserSkillForm


class UserWorkSamplesAdminInline(admin.TabularInline):
    model = UserWorkSamples
    extra = 1
    form = UserWorkSamplesForm


class UserRecommendationAdminInline(admin.StackedInline):
    model = UserRecommendation
    extra = 1
    form = UserRecommendationForm


class UserLanguageAdminInline(admin.TabularInline):
    model = UserLanguage
    extra = 1
    form = UserLanguageForm


class UserSocialMediaAdminInline(admin.TabularInline):
    model = UserSocialMedia
    extra = 2
    form = UserSocialMediaForm


class UserAboutAdminInline(admin.TabularInline):
    model = UserAbout
    extra = 1
    form = UserAboutForm


def active_customer(modeladmin, request, queryset):
    res = queryset.update(is_active=True)
    message = f'تعداد {res} کاربر فعال شد'
    modeladmin.message_user(request, message)


def de_active_customer(modeladmin, request, queryset):
    res = queryset.update(is_active=False)
    message = f'تعداد {res} کاربر غیرفعال شد'
    modeladmin.message_user(request, message)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    form = UserForm
    list_display = ['name', 'family', 'job', 'user_phone', 'age', 'gender_class', 'military_class', 'marital_class',
                    'is_active', 'is_admin', 'country', 'state', 'city']
    list_filter = ['is_active', 'is_admin']
    search_fields = ['name', 'family']
    list_editable = ('is_active',)
    actions = [active_customer, de_active_customer]
    de_active_customer.short_description = 'غیرفعال سازی کاربران انتخابی'
    active_customer.short_description = 'فعال سازی کاربران انتخابی'
    filter_horizontal = ('groups', 'user_permissions')
    inlines = [UserEducationInstanceAdminInline, UserWorkExperienceInstanceAdminInline, UserSkillInstanceAdminInline,
               UserWorkSamplesAdminInline, UserRecommendationAdminInline, UserLanguageAdminInline,
               UserSocialMediaAdminInline, UserAboutAdminInline]


@admin.register(UserEducation)
class UserEducationAdmin(admin.ModelAdmin):
    list_display = ('user', 'grade', 'field_of_study', 'university_name', 'start_date', 'end_date', 'studying')
    list_filter = ('studying',)
    search_fields = ['university_name', 'grade']
    form = UserEducationForm


@admin.register(UserWorkExperience)
class UserWorkExperienceAdmin(admin.ModelAdmin):
    form = UserWorkExperienceForm
    list_display = ('job_title', 'company_name', 'industry', 'side', 'start_date', 'end_date', 'user')
    list_filter = ('side',)
    search_fields = ('job_title', 'side')


@admin.register(UserSkill)
class UserSkillAdmin(admin.ModelAdmin):
    form = UserSkillForm
    list_display = ('user', 'skill_name', 'skill_type', 'skill_rank', 'get_logo')
    list_filter = ('skill_type',)


@admin.register(UserWorkSamples)
class UserWorkSamplesAdmin(admin.ModelAdmin):
    form = UserWorkSamplesForm
    list_display = ('user', 'work_sample_title', 'get_img')


@admin.register(UserRecommendation)
class UserRecommendationAdmin(admin.ModelAdmin):
    form = UserRecommendationForm
    list_display = (
        'user', 'recommender_name', 'relationship_with_recommender', 'recommender_email', 'recommender_phone')


@admin.register(UserLanguage)
class UserLanguageAdmin(admin.ModelAdmin):
    form = UserLanguageForm
    list_display = ('user', 'language', 'read_rank', 'write_rank', 'comprehension_rank')


@admin.register(UserSocialMedia)
class UserSocialMediaAdmin(admin.ModelAdmin):
    form = UserSocialMediaForm
    list_display = ('user', 'social_title', 'link', 'get_logo')


@admin.register(UserAbout)
class UserAboutAdmin(admin.ModelAdmin):
    form = UserAboutForm
    list_display = ('user', 'title')


@admin.register(ContactUs)
class ContactUsAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'phone_number', 'date')


@admin.register(Partner)
class PartnerAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'get_logo')
