from django.forms import ModelForm
from .models import MyUser

class MyUserForm(ModelForm):
	class Meta:
		model = MyUser
		fields = ["name","age","country"]
