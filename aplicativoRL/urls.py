from django.urls import path
from . import views

urlpatterns = [
    path('resultado/', views.executarRegressaoLogistica, name='resultado_rl'),
]
