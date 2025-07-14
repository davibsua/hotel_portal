from django.contrib import admin
from django.urls import path, include

from hotel_portal import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('empleados.urls')),  # todas las rutas de empleados
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)