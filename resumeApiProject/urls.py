from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
                  # region Admin
                  path('admin/', admin.site.urls),
                  # endregion

                  # region admin-CkEditor
                  path('ckeditor', include('ckeditor_uploader.urls')),
                  # endregion

                  # region Swgger
                  path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
                  path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
                  # endregion
                  # path('blogs/', include('apps.blog.urls')),
                  # path('account/', include('apps.accounts.urls')),
                  # path('plans/', include('apps.planing.urls')),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
admin.site.site_header = 'پنل مدیریت رزومه'
