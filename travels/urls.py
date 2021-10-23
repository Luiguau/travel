from django.urls import path
from . import views

urlpatterns = [
	path('', views.index, name='index'),
	path('add', views.add, name='add'),
	path('add_trip', views.add_trip, name='add_trip'),
	path('join', views.join, name='join'),
	path('destination/<int:trip_id>', views.destination, name='destination'),


]