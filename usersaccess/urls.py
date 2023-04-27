from django.urls import path,include
from . import views
from .views import ImageToPDFView

app_name='usersaccess'

urlpatterns = [
    path('login', views.login_view, name='login'),
    path('logout', views.logout_view, name='logout'),
    path('register', views.register_view, name='register'),
    path('register_lawyer', views.register_lawyer_view, name='register_lawyer'),
    path('home', views.landing_view, name='home'),
    path('new_will', views.create_new_will, name='new_will'),
    path('edit_will/<id>', views.edit_will_view, name='edit_will'),
    path('edit_own_will', views.edit_own_will_view, name='edit_own_will'),
    path('render_will', views.render_will_view, name='render_will'),
    path('image-to-pdf', ImageToPDFView.as_view(), name='image-to-pdf'),
    path('handle_dc/<id>', views.handleDC, name='handle_dc'),
    path('schedule_call/<id>', views.scheduleCall, name='schedule_call'),

    path('lobby', views.new_lobby, name='lobby'),



    # path('room/', views.room),
    # path('lobby/', views.lobby),


]