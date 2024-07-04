from django.db import models
from django_jalali.db import models as jmodels
import jdatetime

from apps.accounts.models import User
from ckeditor_uploader.fields import RichTextUploadingField
from django.utils.html import mark_safe


class BlogCategory(models.Model):
    title = models.CharField(max_length=800, verbose_name='عنوان')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'دسته بندی مقاله'
        verbose_name_plural = 'دسته بندی مقالات'


class Blog(models.Model):
    title = models.CharField(max_length=800, verbose_name='عنوان')
    content = RichTextUploadingField(config_name='special', verbose_name='محتوا')
    created_at = jmodels.jDateField(default=jdatetime.date.today(), verbose_name='تاریخ ساخت مقاله')
    pub_date = jmodels.jDateField(blank=True, null=True, verbose_name='تاریخ انتشار')
    is_published = models.BooleanField(default=False, verbose_name='وضعیت انتشار (یافت/نیافت)')
    is_active = models.BooleanField(default=False, verbose_name='وضعیت(فعال/غیرفعال)')
    cover_image = models.ImageField(upload_to='blog/cover', verbose_name='تصویر اصلی')
    alt_attr = models.CharField(max_length=1000, verbose_name='متن جایگزین کاور')
    title_attr = models.CharField(max_length=1000, verbose_name='عنوان کاور')
    view_count = models.IntegerField(default=1, verbose_name='تعداد بازدید')
    category = models.ForeignKey(BlogCategory, on_delete=models.CASCADE, related_name='blog_categories',
                                 verbose_name='دسته بندی')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_user', verbose_name='نویسنده')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'مقاله'
        verbose_name_plural = 'مقالات'

    def get_seo(self):
        return list(self.blog_seo.all())

    def get_blog_img(self):
        return mark_safe(
            '<img src="/media/%s" width="50" height="50" style="border-radius:5px;" />' % self.cover_image)

    get_blog_img.short_description = 'کاور مقاله'
    get_blog_img.allow_tags = True

    def show_seo(self):
        return mark_safe(
            f'<a style="border-radius: 5px;background-color: #417690;padding: 5px 11px;font-weight: 450; color:#fff;" href="{utilities.base_url}admin/blog/blogseo/?blog_id={self.id}">مشاهده سئو</a>')

    show_seo.short_description = ''
    show_seo.allow_tags = True

    def show_tag(self):
        return mark_safe(
            f'<a style="border-radius: 5px;background-color: #417690;padding: 5px 11px;font-weight: 450; color:#fff;" href="{utilities.base_url}admin/blog/blogtag/?blog_id={self.id}">مشاهده تگ</a>')

    show_tag.short_description = ''
    show_tag.allow_tags = True

    def save(self, *args, **kwargs):
        if self.is_published:
            self.pub_date = jdatetime.date.today()
        super().save(*args, **kwargs)


class BlogSeo(models.Model):
    SEO_TYPE = (('name', 'name'), ('property', 'property'))
    title = models.CharField(max_length=1000, verbose_name='عنوان')
    type = models.CharField(max_length=1000, choices=SEO_TYPE, verbose_name='نوع')
    content = models.TextField(verbose_name='محتوا')
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='blog_seo', verbose_name='مقاله')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'سئو مقاله'
        verbose_name_plural = 'سئو مقالات'


class BlogTag(models.Model):
    title = models.CharField(max_length=1000, verbose_name='عنوان')
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='blog_tags', verbose_name='مقاله')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'تگ مقاله'
        verbose_name_plural = 'تگ مقالات'
