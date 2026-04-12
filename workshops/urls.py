from django.urls import path
from . import views

urlpatterns =[
    path('', views.WorkshopList.as_view(), name='home'),
]