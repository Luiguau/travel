from django.shortcuts import render,redirect
from django.contrib import messages
from .models import *


# Create your views here.
def index(request):
	if 'user_id' not in request.session:
		return redirect('/')
	context = {
			"my_trips": Trip.objects.filter(creator=request.session['user_id']) | Trip.objects.filter(joined_user=request.session['user_id']) ,
			"other_trips": Trip.objects.exclude(creator=request.session['user_id']) & Trip.objects.exclude(joined_user=request.session['user_id']),
	}
	return render(request, 'travels.html', context)
	

def add(request):
	return render(request, 'add.html')


def add_trip(request):
	errors = Trip.objects.basic_validator(request.POST)
	if len(errors) > 0:
		for key, msg in errors.items():
			messages.error(request, msg, extra_tags=key)
		return redirect('/travels/add')
	trip=Trip.objects.create(
		creator= User.objects.get(id=request.session['user_id']),
		destination=request.POST['dest'],
		description=request.POST['descript'],
		start_date=request.POST['dfrom'],
		end_date=request.POST['dto']
	)
	return redirect('/')


def join(request):
	trip=Trip.objects.get(id=request.POST['trip_id'])
	user=User.objects.get(id=request.session['user_id'])
	trip.joined_user.add(user)
	return redirect('/')


def destination(request, trip_id):
	context = {
		"trip":Trip.objects.get(id=trip_id),
	}
	return render(request,"destination.html", context)