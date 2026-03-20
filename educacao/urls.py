from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_recursos, name='lista_recursos'),
    path('criar/', views.criar_recurso, name='criar_recurso'),
    path('<int:pk>/editar/', views.editar_recurso, name='editar_recurso'),
    path('<int:pk>/deletar/', views.deletar_recurso, name='deletar_recurso'),
]