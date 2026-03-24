from django.urls import path
from . import views
from .views import SignupView, CompleteProfileView, EditProfileView, AcessibilidadeView, ConfiguracoesView, CustomLoginView

urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('signup/complete/', CompleteProfileView.as_view(), name='complete_profile'),
    path('perfil/editar/', EditProfileView.as_view(), name='editar_perfil'),
    path('perfil/<slug:slug>/', views.perfil_usuario, name='perfil_usuario'),
    path('acessibilidade/', AcessibilidadeView.as_view(), name='acessibilidade'),
    path('configuracoes/', ConfiguracoesView.as_view(), name='configuracoes'), 
    path('login/', CustomLoginView.as_view(), name='login'),
]