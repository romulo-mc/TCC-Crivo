from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('pesquisa/', views.pesquisa_geral, name='pesquisa_geral'),
    path('notificacoes/', views.lista_notificacoes, name='lista_notificacoes'),
    path('notificacoes/lidas/', views.marcar_todas_lidas, name='marcar_todas_lidas'),
    path('notificacoes/ir/<int:pk>/', views.marcar_lida_e_ir, name='marcar_lida_e_ir'),
    path('notificacoes/limpar/', views.limpar_notificacoes, name='limpar_notificacoes'),
    path('moderacao/', views.painel_moderacao, name='painel_moderacao'),
]