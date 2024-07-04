from django.urls import include, path, re_path
from . import views

urlpatterns = [
    path('', views.BlogApiView.as_view(), name='blog'),
    re_path(r'^by-slug/(?P<slug>[^/]+)/$', views.BlogDetailBySlugApiView.as_view(), name='blog-detail-slug'),
    path('by-id/<int:id>', views.BlogDetailByIdApiView.as_view(), name='blog-detail-id'),
]
