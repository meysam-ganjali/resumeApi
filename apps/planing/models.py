from django.db import models
from apps.accounts.models import User


class Planing(models.Model):
    planning_type = models.CharField(max_length=500, verbose_name="نوع پلن")
    validity = models.CharField(max_length=500, null=True, blank=True,
                                help_text='مانند : هفته ای، ماهانه ، سالانه و...', verbose_name="مدت اعتبار")
    planing_price = models.PositiveIntegerField(verbose_name="قیمت")
    planing_name = models.CharField(max_length=500, verbose_name="نام پلن")
    logo = models.ImageField(upload_to='users/plans/', verbose_name="تصویر", null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="کاربر", related_name="planing")

    def __str__(self):
        return f'{self.user.name} {self.user.family} : {self.planing_name} {self.planing_price}'

    class Meta:
        verbose_name = "پلن فروش"
        verbose_name_plural = "پلن های فروش"


class PlaningFeature(models.Model):
    feature_name = models.CharField(max_length=500, verbose_name="نام مشخصه")
    feature_value = models.CharField(max_length=500, verbose_name="مقدار مشخصه")
    planing = models.ForeignKey(Planing, on_delete=models.CASCADE, verbose_name="پلن", related_name="planing_feature")

    def __str__(self):
        return f'{self.planing.planing_name} ({self.planing.user.name} {self.planing.user.family}): {self.feature_name}'

    class Meta:
        verbose_name = "ویژگی پلن"
        verbose_name_plural = "ویژگی های پلن"
