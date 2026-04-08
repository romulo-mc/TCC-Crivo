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
    path('moderacao/aprovar/<str:tipo>/<int:item_id>/', views.aprovar_item, name='aprovar_item'),
    path('moderacao/rejeitar/<str:tipo>/<int:item_id>/', views.rejeitar_item, name='rejeitar_item'),
    path('moderacao/aprovar-massa/', views.aprovar_massa, name='aprovar_massa'),
    path('moderacao/usuario/<int:user_id>/toggle-ban/', views.toggle_ban_usuario, name='toggle_ban_usuario'),
    
    path('moderacao/tag/adicionar/', views.adicionar_tag_moderacao, name='adicionar_tag_moderacao'),
    path('moderacao/tag/editar/', views.editar_tag_moderacao, name='editar_tag_moderacao'),
    path('moderacao/tag/excluir/<str:tipo>/<int:tag_id>/', views.excluir_tag_moderacao, name='excluir_tag_moderacao'),
]