from django.urls import path
from . import views

urlpatterns = [
    path('adicionar/', views.adicionar_item, name='adicionar_item'),
]