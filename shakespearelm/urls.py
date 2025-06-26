# myapp/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("ajax/generate", views.generate, name="generate"),
]
