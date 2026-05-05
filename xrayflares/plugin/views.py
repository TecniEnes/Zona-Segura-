from django.shortcuts import render
from django.http import HttpResponse 
from .models import Flux
from datetime import datetime
# Create your views here.

def index(request):
	data= Flux.objects.values()
	now = datetime.now()
	flux = Flux(now, 1.0,"hello")
	flux.save()
	return HttpResponse(data,content_type='application/json')
