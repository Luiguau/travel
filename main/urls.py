from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('registrar', views.registrar, name='registrar'),
    path('login', views.login, name='login'),
    path('registro', views.registro, name='registro'),
    path('logout', views.logout, name='logout'),
    path('cambiar_pass', views.cambiar_pass, name='cambiar_pass'),
    path('change', views.change, name='change'),
]