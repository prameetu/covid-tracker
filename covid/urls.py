from os import name
from django.urls import path

from covid import views

app_name = 'app4'

urlpatterns = [
    path('', views.state_wise, name='cases'),
    path('<str:num>/',views.state_wise1)
]