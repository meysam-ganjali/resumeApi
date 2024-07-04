from django.contrib import admin
from .models import Blog, BlogSeo, BlogTag, BlogCategory
from django.db.models.aggregates import Count


class BlogSeoInstanceAdminInline(admin.TabularInline):
    model = BlogSeo
    extra = 2


class BlogtagInstanceAdminInline(admin.TabularInline):
    model = BlogTag
    extra = 2


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = (
        'title', 'get_blog_img', 'created_at', 'pub_date', 'is_published', 'is_active', 'show_seo', 'show_tag')
    inlines = [BlogSeoInstanceAdminInline, BlogtagInstanceAdminInline]
    ordering = ('-pub_date', 'title') # This should populate 'slug' from 'title'
    list_filter = ('is_published', 'is_active')
    list_editable = ('is_published', 'is_active')


@admin.register(BlogSeo)
class BlogSeoAdmin(admin.ModelAdmin):
    list_display = ('title', 'type', 'content', 'blog')


@admin.register(BlogTag)
class BlogTagAdmin(admin.ModelAdmin):
    list_display = ('title', 'blog')


@admin.register(BlogCategory)
class BlogCategory(admin.ModelAdmin):
    list_display = ('title', 'blog_count')

    def get_queryset(self, *args, **kwargs):
        qs = super(BlogCategory, self).get_queryset(*args, **kwargs)
        qs = qs.annotate(blogs_count=Count('blog_categories'))
        return qs

    def blog_count(self, obj):
        return obj.blogs_count

    blog_count.short_description = 'تعداد مقاله در دسته بندی'
