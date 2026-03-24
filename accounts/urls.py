from django.urls import path
from . import views
from .views import SignupView, CompleteProfileView, AcessibilidadeView, ConfiguracoesView
urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('signup/complete/', CompleteProfileView.as_view(), name='complete_profile'),
    path('perfil/editar/', views.CompleteProfileView.as_view(), name='complete_profile'),
    path('perfil/<slug:slug>/', views.perfil_usuario, name='perfil_usuario'),
    path('acessibilidade/', AcessibilidadeView.as_view(), name='acessibilidade'),
    path('configuracoes/', ConfiguracoesView.as_view(), name='configuracoes'),
]