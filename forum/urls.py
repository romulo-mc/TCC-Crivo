from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_forum, name='lista_forum'),
    path('novo/', views.criar_topico, name='criar_topico'),
    path('topico/<slug:slug>/', views.detalhe_topico, name='detalhe_topico'),
    path('topico/<slug:slug>/votar/<str:tipo>/', views.votar_topico, name='votar_topico'),
    path('resposta/<int:id>/votar/<str:tipo>/', views.votar_resposta, name='votar_resposta'),
    path('topico/<slug:slug>/editar/', views.editar_topico, name='editar_topico'),
    path('resposta/<int:id>/editar/', views.editar_resposta, name='editar_resposta'),
]