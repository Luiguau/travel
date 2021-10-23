from django.db import models
from datetime import datetime

from main.models import User
# Create your models here.
class TripManager(models.Manager):
	def basic_validator(self, postData):
		errores = {}
		if len(postData['dest']) == 0:
			errores['dest'] = "Please choose a destination"
		if len(postData['descript']) == 0:
			errores['descript'] = "Please choose a description"
		Pf=postData['dfrom'].split('-')
		Pt=postData['dto'].split('-')
		if datetime(int(Pf[0]),int(Pf[1]),int(Pf[2])) < datetime.now():
			errores['dfrom'] = '"Date from" should be a future date'
		if datetime(int(Pt[0]),int(Pt[1]),int(Pt[2])) < datetime(int(Pf[0]),int(Pf[1]),int(Pf[2])):
			errores['dto'] = '"Date to" has to be after "date from"'

		return errores


class Trip(models.Model):
	creator = models.ForeignKey(User, related_name="creator", on_delete=models.CASCADE)
	destination = models.CharField(max_length=255)
	description = models.CharField(max_length=255)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	start_date = models.DateField()
	end_date = models.DateField()
	joined_user = models.ManyToManyField(User, related_name="users", blank=True, null=True)
	objects = TripManager()