from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_forum, name='lista_forum'),
    path('topico/<slug:slug>/', views.detalhe_topico, name='detalhe_topico'),
    path('topico/<slug:slug>/curtir/', views.curtir_topico, name='curtir_topico'),
]