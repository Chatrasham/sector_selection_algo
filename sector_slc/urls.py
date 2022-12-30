from django.contrib import admin
from django.urls import path

from fetch_data.urls import urlpatterns as fetch_data_urlpatterns

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
] + fetch_data_urlpatterns 
if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)