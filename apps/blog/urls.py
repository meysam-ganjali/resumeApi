from django.urls import include, path, re_path
from . import views

urlpatterns = [
    path('', views.BlogApiView.as_view(), name='blog'),
    path('by-id/<int:id>', views.BlogDetailByIdApiView.as_view(), name='blog-detail-id'),
]
