from rest_framework import serializers
from .models import Blog, BlogTag, BlogSeo, BlogCategory
from apps.accounts.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'family', 'image']


class BlogCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogCategory
        fields = '__all__'


class BlogTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogTag
        fields = '__all__'


class BlogSeoSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogSeo
        fields = '__all__'


class BlogSerializer(serializers.ModelSerializer):
    category = BlogCategorySerializer()
    author = UserSerializer()
    tags = serializers.SerializerMethodField()
    seos = serializers.SerializerMethodField()

    class Meta:
        model = Blog
        fields = ['id', 'title', 'slug', 'content', 'created_at', 'pub_date', 'cover_image', 'alt_attr', 'title_attr',
                  'view_count', 'category', 'author', 'tags', 'seos']

    def get_tags(self, obj):
        tags = obj.blog_tags.all()
        return BlogTagSerializer(tags, many=True).data

    def get_seos(self, obj):
        seos = obj.blog_seo.all()
        return BlogSeoSerializer(seos, many=True).data
