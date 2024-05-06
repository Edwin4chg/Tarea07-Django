from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Otras rutas de la aplicación...
    path('', views.user_login, name='login'),    
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('home', views.home, name='home'),
    
    path('crear_evento/', views.crear_evento, name='crear_evento'),
    path('registro_evento/', views.registro_evento, name='registro_evento'),
    path('detalles_eventos/', views.detalles_eventos, name='detalles_eventos'),
    path('mis_registros_eventos/', views.mis_registros_eventos, name='mis_registros_eventos'),
]