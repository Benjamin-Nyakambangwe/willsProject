from django.urls import path,include
from . import views

app_name='usersaccess'

urlpatterns = [
    path('login', views.login_view, name='login'),
    path('logout', views.logout_view, name='logout'),
    path('register', views.register_view, name='register'),
    path('register_lawyer', views.register_lawyer_view, name='register_lawyer'),
    path('home', views.landing_view, name='home'),
    path('new_will', views.create_new_will, name='new_will'),
    path('render_will', views.render_will_view, name='render_will'),

]