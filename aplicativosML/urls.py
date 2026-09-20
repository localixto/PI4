from django.urls import path
from . import views

urlpatterns= [
    path('nb/', views.algoritmoNB, name="algNB"),    
]