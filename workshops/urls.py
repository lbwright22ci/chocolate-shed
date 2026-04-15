from django.urls import path
from . import views

urlpatterns =[
    path('', views.WorkshopList.as_view(), name='home'),
    path('children/', views.ChildrensWorkshopList.as_view(), name="child_workshops"),
    path('family/', views.FamilyWorkshopList.as_view(), name="family_workshops"),
    path('adult/', views.AdultWorkshopList.as_view(), name="adult_workshops"),
    path("<slug:slug>/", views.WorkshopDetailView.as_view(), name="workshop_detail")
]