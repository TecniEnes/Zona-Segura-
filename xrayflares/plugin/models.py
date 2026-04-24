from django.db import models

# Create your models here.
class Flux(models.Model):
	date_time= models.DateTimeField("date time", primary_key=True)
	flux = models.FloatField(default=0.0)

