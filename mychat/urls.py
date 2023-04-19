from django.contrib import admin
from django.urls import path, include
from usersaccess.views import landing_view

urlpatterns = [
    path('', landing_view, name='home'),
    path('admin/', admin.site.urls),
    path('', include('base.urls')),
    path('', include('usersaccess.urls'))
]
