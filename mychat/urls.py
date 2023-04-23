from django.contrib import admin
from django.urls import path, include
from usersaccess.views import landing_view
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', landing_view, name='home'),
    path('admin/', admin.site.urls),
    path('', include('base.urls')),
    path('', include('usersaccess.urls', namespace="usersaccess")),
    path('', include('django.contrib.auth.urls')),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
