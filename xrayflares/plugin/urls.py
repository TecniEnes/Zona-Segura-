from django.urls import path
from . import views 
from .views import MyUserView
urlpatterns = [re_path(r're_path(r'^(?P<isbn>[^/])+)/api/s', MyUserView.as_view()), path("", views.index, name="index"),]

]
