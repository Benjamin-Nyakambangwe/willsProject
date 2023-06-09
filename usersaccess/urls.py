from django.urls import path,include
from . import views
from .views import ImageToPDFView

app_name='usersaccess'

urlpatterns = [
    path('login', views.login_view, name='login'),
    path('logout', views.logout_view, name='logout'),
    path('register', views.register_view, name='register'),
    path('register_lawyer', views.register_lawyer_view, name='register_lawyer'),
    path('register_executor', views.register_executor_view, name='register_executor'),
    path('home', views.landing_view, name='home'),
    path('new_will', views.create_new_will, name='new_will'),
    path('edit_will/<id>', views.edit_will_view, name='edit_will'),
    path('edit_own_will', views.edit_own_will_view, name='edit_own_will'),
    path('render_will', views.render_will_view, name='render_will'),
    path('image-to-pdf', ImageToPDFView.as_view(), name='image-to-pdf'),
    path('handle_dc/<id>', views.handleDC, name='handle_dc'),
    path('schedule_call/<id>', views.scheduleCall, name='schedule_call'),
    path('owner_sign', views.owner_sign_view, name='owner_sign'),
    path('executor_sign', views.executor_sign_view, name='executor_sign'),
    path('lawyer_sign/<id>', views.lawyer_sign_view, name='lawyer_sign'),
    path('image_to_text/<id>', views.image_to_text, name='image_to_text'),
    path('lobby', views.new_lobby, name='lobby'),



    # path('room/', views.room),
    # path('lobby/', views.lobby),


]