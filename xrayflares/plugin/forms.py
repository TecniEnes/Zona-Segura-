from django.forms import ModelForm
from .models import MyUser

class MyUserForm(ModelFrom):
	class Meta:
		model = MyUser
		fields = ["name","age","country"]
