from django.urls import path
from . import views

urlpatterns = [
    path('bug/reportar/', views.reportar_bug, name='reportar_bug'),
    path('avaliar/', views.avaliar_plataforma, name='avaliar_plataforma'),
]