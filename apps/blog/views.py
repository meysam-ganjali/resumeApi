from django.shortcuts import render
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Blog, BlogCategory
from apps.utilities import response_formatter, CustomPagination
from .serializer import BlogSerializer, BlogCategorySerializer
from django.utils.encoding import uri_to_iri


class BlogApiView(APIView):
    @extend_schema(
        request=BlogSerializer,
        responses={200: BlogSerializer(many=True)},
        parameters=[
            OpenApiParameter(name='tag_id', type=OpenApiTypes.INT, location=OpenApiParameter.QUERY,
                             description='جستجوی مقالات بر اساس آی دی تگ'),
            OpenApiParameter(name='category_id', type=OpenApiTypes.INT, location=OpenApiParameter.QUERY,
                             description='جستجو براساس آی دی دسته بندی'),
            OpenApiParameter(name='مرتب سازی', type=OpenApiTypes.STR, location=OpenApiParameter.QUERY,
                             description='Ordering (e.g. "pub_date", "-pub_date", "view_count", "-view_count")'),
        ]
    )
    def get(self, request):
        data = {}
        tag_id = request.GET.get('tag_id', None)
        category_id = request.GET.get('category_id', None)
        ordering = request.GET.get('ordering', None)
        blogs = Blog.objects.all()
        if tag_id is not None:
            blogs = blogs.filter(blog_tags__id=tag_id)
        if category_id is not None:
            blogs = blogs.filter(category_id=category_id)
        if ordering:
            blogs = blogs.order_by(ordering)
        paginator = CustomPagination()
        paginated_blogs = paginator.paginate_queryset(blogs, request)
        blog_serializer = BlogSerializer(paginated_blogs, many=True)
        blog_categories = BlogCategory.objects.all()
        blog_category_serializer = BlogCategorySerializer(blog_categories, many=True)
        data['blogs'] = blog_serializer.data
        data['blog_categories'] = blog_category_serializer.data
        return paginator.get_paginated_response(response_formatter(data, status.HTTP_200_OK, 'لیست مقالات'))


class BlogDetailByIdApiView(APIView):
    @extend_schema(
        request=BlogSerializer,
        responses={200: BlogSerializer(many=False)},
    )
    def get(self, request, id: int):
        try:
            blog = Blog.objects.get(id=id)
            serializer = BlogSerializer(blog, many=False)
            return Response(response_formatter(serializer.data, status.HTTP_200_OK, 'جزئیات مقاله'))
        except Blog.DoesNotExist:
            return Response(response_formatter(None, status.HTTP_404_NOT_FOUND, 'مقاله یافت نشد'))
