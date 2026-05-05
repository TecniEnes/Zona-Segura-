from django.shortcuts import render
from django.http import HttpResponse 
from .models import Flux
from datetime import datetime
from .forms import MyUserForm
from datetime import datetime
from django.views.generic import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
# Create your views here.
#123
def index(request):
	data= Flux.objects.values()
	now = datetime.now()
	flux = Flux(now, 1.0,"hello")
	flux.save()
	return HttpResponse(data,content_type='application/json')

class MyUserView(View):
	form_class = MyUserForm
	template_name = 'plugin/info.html'

	###@method_decorator(login_required)
	def dispatch(self,*args,**kwargs):
		return super(Book_View, self).dispatch(*args, **kwargs)
	#return HttpResponse(data,content_type='application/json')
	
