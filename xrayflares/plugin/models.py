from django.db import models
import uuid
from django_countries.fields import CountryField
# Create your models here.
class Flux(models.Model):
	date_time= models.DateTimeField("date time", primary_key=True)
	flux = models.FloatField(default=0.0)
	name = models.CharField(max_length=128, default="")

class  MyUser(models.Model):
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	name=models.CharField(max_length=128, default="")
	age=models.IntegerField(default=18)
	country= CountryField()
