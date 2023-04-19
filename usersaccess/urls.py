from django.urls import path,include
from . import views

app_name='usersaccess'

urlpatterns = [
    path('login', views.login_view, name='login'),
    path('home', views.landing_view, name='home'),
    path('new_will', views.create_new_will, name='new_will'),

]