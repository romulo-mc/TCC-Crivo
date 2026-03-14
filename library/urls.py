from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_library, name='lista_library'),
    path('adicionar/', views.adicionar_item, name='adicionar_item'),
    path('item/<int:id>/', views.detalhe_item, name='detalhe_item'),
    path('item/<int:id>/editar/', views.editar_item, name='editar_item'),
    path('review/<int:id>/editar/', views.editar_review, name='editar_review'),
]