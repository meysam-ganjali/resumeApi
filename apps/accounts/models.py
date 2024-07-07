from ckeditor.fields import RichTextField
from django.utils.safestring import mark_safe
from django_jalali.db import models as jmodels
import jdatetime
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, user_phone, email='', name='', family='', active_code=None, password=None):
        if not user_phone:
            raise ValueError('شماره موبایل را وارد نکرده اید')
        user = self.model(user_phone=user_phone, email=self.normalize_email(email), name=name, family=family,
                          active_code=active_code)
        if len(password) < 6:
            raise ValueError('طول کلمه عبور باید بیشتر از 6 باشد')

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, user_phone, email, name, family, password=None, active_code=None):
        user = self.create_user(user_phone, email, name, family, active_code, password)
        user.is_active = True
        user.is_admin = True
        user.is_superuser = True

        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    GENDER_CHOICES = (('M', 'آقا'), ('F', 'خانم'), ('O', 'دیگر'))
    MARITAL_CLASS_CHOICES = (('MARRIED', 'متاهل'), ('SINGLE', 'مجرد'), ('DIVORCED', 'مطلقه'))
    MILITARY_CHOICES = (
        ('EP', 'معافیت تحصیلی'), ('SE', 'معافیت خاص'), ('ME', 'معافیت پزشکی'), ('TEOS', 'پایان خدمت'), ('I', 'مشمول'),
        ('NI', 'شامل من نمیشه'))
    user_phone = models.CharField(max_length=15, unique=True, verbose_name='شماره موبایل')
    email = models.CharField(blank=True, null=True, max_length=200, verbose_name='ایمیل')
    name = models.CharField(max_length=50, verbose_name='نام')
    family = models.CharField(max_length=50, verbose_name='نام خانوادگی')
    image = models.ImageField(upload_to='users/logo/', verbose_name='عکس پروفایل کاربری', blank=True, null=True)
    gender_class = models.CharField(max_length=10, blank=True, null=True, choices=GENDER_CHOICES, verbose_name='جنسیت')
    military_class = models.CharField(max_length=10, blank=True, null=True, choices=MILITARY_CHOICES,
                                      verbose_name='وضعیت خدمت')
    marital_class = models.CharField(max_length=10, blank=True, null=True, choices=MARITAL_CLASS_CHOICES,
                                     verbose_name='وضعیت ازدواج')
    register_date = jmodels.jDateField(default=jdatetime.date.today(), verbose_name='تاریخ ثبت نام')
    birth_date = jmodels.jDateField(blank=True, null=True, verbose_name='تاریخ تولد')
    country = models.CharField(max_length=5000, blank=True, null=True, verbose_name='کشور')
    city = models.CharField(blank=True, null=True, max_length=5000, verbose_name='شهر')
    state = models.CharField(blank=True, null=True, max_length=5000, verbose_name='استان')
    job = models.CharField(blank=True, null=True, max_length=100, verbose_name='شغل')
    requested_salary = models.PositiveIntegerField(blank=True, null=True, verbose_name='حقوق درخواستی')
    show_salary = models.BooleanField(blank=True, null=True, default=False, verbose_name='نمایش حقوق در رزومه')
    age = models.PositiveSmallIntegerField(verbose_name='سن', blank=True, null=True)
    active_code = models.CharField(max_length=10, blank=True, null=True, )
    is_active = models.BooleanField(default=False, verbose_name='وضعیت کاربر')
    is_admin = models.BooleanField(default=False)
    USERNAME_FIELD = 'user_phone'
    REQUIRED_FIELDS = ['name', 'family', 'email']
    objects = UserManager()

    def get_gender_class_display_value(self):
        return self.get_gender_class_display()

    def get_marital_class_display_value(self):
        return self.get_marital_class_display()

    def get_military_class_display_value(self):
        return self.get_military_class_display()

    class Meta:
        verbose_name = 'کاربر'
        verbose_name_plural = 'کاربران'

    def __str__(self):
        return f'{self.name} - {self.family}'

    def has_perms(self, perm_list, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin

    def get_user_img(self):
        if self.image:
            return mark_safe(
                '<img src="/media/%s" width="50" height="50" style="border-radius:5px;" />' % self.image)
        else:
            return mark_safe(
                '<img src="/media/%s" width="50" height="50" style="border-radius:5px;" />' % 'no_image.jpg')

    get_user_img.short_description = 'تصویر'
    get_user_img.allow_tags = True


class UserEducation(models.Model):
    grade = models.CharField(max_length=1000, verbose_name='مقطع تحصیلی')
    field_of_study = models.CharField(max_length=1000, verbose_name='رشته تحصیلی')
    university_name = models.CharField(max_length=1000, verbose_name='نام دانشگاه')
    start_date = jmodels.jDateField(verbose_name='تاریخ شروع')
    end_date = jmodels.jDateField(blank=True, null=True, verbose_name='تاریخ فارغ التحصیل')
    studying = models.BooleanField(default=False, verbose_name='در حال تحصیل')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='کاربر', related_name='user_education')

    def __str__(self):
        return f'{self.user.name} {self.user.family} : {self.university_name} {self.grade} {self.field_of_study}'

    class Meta:
        verbose_name = 'تحصیل کاربر'
        verbose_name_plural = 'تحصیلات کاربران'


class UserWorkExperience(models.Model):
    job_title = models.CharField(max_length=500, verbose_name='عنوان شغل')
    company_name = models.CharField(max_length=500, verbose_name='نام شرکت')
    industry = models.CharField(max_length=500, verbose_name='صنعت')
    side = models.CharField(max_length=500, verbose_name='سمت')
    start_date = jmodels.jDateField(verbose_name='تاریخ شروع')
    end_date = jmodels.jDateField(blank=True, null=True, verbose_name='تاریخ ترک شغل')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='', related_name='user_experience')

    class Meta:
        verbose_name = 'سابقه شغل'
        verbose_name_plural = 'سوابق شغلی'

    def __str__(self):
        return f'{self.user.name} {self.user.family} : {self.job_title} {self.start_date} {self.end_date}'


class UserSkill(models.Model):
    SKILL_CHOICES = (('H', 'سخت'), ('S', 'نرم'))
    skill_name = models.CharField(max_length=500, verbose_name='عنوان مهارت')
    skill_type = models.CharField(max_length=1, choices=SKILL_CHOICES, verbose_name='نوع مهارت')
    skill_rank = models.IntegerField(help_text='این فیلد بین 1 تا 5 پر میشود', verbose_name='درجه تسلط')
    skill_logo = models.ImageField(upload_to='users/skill/', blank=True, null=True, verbose_name='لگو مهارت')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='کاربر', related_name='user_skill')

    def __str__(self):
        return f'{self.user.name} {self.user.family} : {self.skill_name}-{self.skill_type} {self.skill_rank}'

    class Meta:
        verbose_name = 'مهارت کاربر'
        verbose_name_plural = 'مهارت کاربران'

    def get_logo(self):
        if self.skill_logo:
            return mark_safe(
                '<img src="/media/%s" width="50" height="50" style="border-radius:5px;" />' % self.skill_logo)
        else:
            return mark_safe(
                '<img src="/media/%s" width="50" height="50" style="border-radius:5px;" />' % 'no_image.jpg')


class UserWorkSamples(models.Model):
    work_sample_title = models.CharField(max_length=500, verbose_name='عنوان نمونه کار')
    work_sample_description = RichTextField(config_name='special', verbose_name='توضیحات')
    work_sample_image = models.ImageField(upload_to='users/work/', blank=True, null=True,
                                          verbose_name='تصویر نمونه کار')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='کاربر', related_name='user_work_samples')

    def __str__(self):
        return f'{self.user.name} {self.user.family}: {self.work_sample_title}'

    class Meta:
        verbose_name = 'نمونه کار'
        verbose_name_plural = 'نمونه کارها'

    def get_img(self):
        if self.work_sample_image:
            return mark_safe(
                '<img src="/media/%s" width="100" height="100" style="border-radius:5px;" />' % self.work_sample_image)

    get_img.short_description = ''


class UserRecommendation(models.Model):
    recommender_name = models.CharField(max_length=500, verbose_name='نام توصیه کننده')
    relationship_with_recommender = models.CharField(max_length=500, verbose_name='نوع رابطه با توصیه کننده')
    recommender_email = models.EmailField(max_length=500, verbose_name='ایمیل توصیه کننده')
    recommender_phone = models.CharField(max_length=15, verbose_name='تلفن توصیه کننده')
    request_text = RichTextField(config_name='special', verbose_name='متن درخواست')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='کاربر', related_name='user_recommendations')

    def __str__(self):
        return f'{self.user.name} {self.user.family}: {self.recommender_name}'

    class Meta:
        verbose_name = 'توصیه نامه'
        verbose_name_plural = 'توصیه نامه ها'


class UserLanguage(models.Model):
    language = models.CharField(max_length=100, verbose_name='عنوان زبان')
    read_rank = models.IntegerField(help_text='این فیلد بین 1 تا 5 پر میشود', default=1,
                                    verbose_name='درجه تسلط خواندن')
    write_rank = models.IntegerField(help_text='این فیلد بین 1 تا 5 پر میشود', default=1,
                                     verbose_name='درجه تسلط نوشتن')
    comprehension_rank = models.IntegerField(help_text='این فیلد بین 1 تا 5 پر میشود', default=1,
                                             verbose_name='درجه درک مطلب')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='کاربر', related_name='user_languages')

    def __str__(self):
        return f'{self.user.name} {self.user.family}: {self.language} {str(self.read_rank)}'

    class Meta:
        verbose_name = 'مهارت زبان'
        verbose_name_plural = 'مهارت های زبان'


class UserSocialMedia(models.Model):
    social_title = models.CharField(max_length=5000, verbose_name='عنوان')
    link = models.CharField(max_length=500, verbose_name='لینک')
    logo = models.ImageField(upload_to='users/social/', verbose_name='لگو')
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, verbose_name='کاربر',
                             related_name='social_media')

    def __str__(self):
        return f'{self.user.name} {self.user.family}: {self.social_title}'

    class Meta:
        verbose_name = 'شبکه اجتماعی کاربر'
        verbose_name_plural = 'شبکه اجتماعی کاربران'

    def get_logo(self):
        return mark_safe(
            '<img src="/media/%s" width="50" height="50" style="border-radius:5px;" />' % self.logo)

    get_logo.short_description = ''


class UserAbout(models.Model):
    title = models.CharField(max_length=5000, verbose_name='عنوان')
    description = RichTextField(config_name='special', verbose_name='متن درباره من')
    user = models.OneToOneField(to=User, on_delete=models.CASCADE, verbose_name='کاربر', related_name='about')

    def __str__(self):
        return f'{self.user.name} {self.user.family} : {self.title}'

    class Meta:
        verbose_name = 'درباره کاربر'
        verbose_name_plural = 'درباره کاربران'


class ContactUs(models.Model):
    full_name = models.CharField(max_length=500, verbose_name='نام . نام خانوادگی')
    phone_number = models.CharField(max_length=15, verbose_name='شماره تلفن همراه')
    request_text = RichTextField(config_name='special',verbose_name='متن درخواست')
    date = jmodels.jDateField(default=jdatetime.date.today(), verbose_name='تاریخ درخواست')

    def __str__(self):
        return f'{self.full_name} {self.phone_number}'

    class Meta:
        verbose_name = 'تماس با ما'
        verbose_name_plural = 'لیست تماس با ما'


class Partner(models.Model):
    name = models.CharField(max_length=500, verbose_name='نام همکار')
    description = models.TextField(verbose_name='توضیحات')
    logo = models.ImageField(upload_to='users/partners/', help_text='این فیلد اختیاری می باشد.', verbose_name='لگو',
                             blank=True, null=True)
    user = models.OneToOneField(to=User, on_delete=models.CASCADE, verbose_name='کاربر', related_name='partner')

    def __str__(self):
        return f'{self.user} : {self.name}'

    def get_logo(self):
        return mark_safe(
            '<img src="/media/%s" width="50" height="50" style="border-radius:5px;" />' % self.logo)

    get_logo.short_description = ''

    class Meta:
        verbose_name = 'همکار'
        verbose_name_plural = 'همکاران'
