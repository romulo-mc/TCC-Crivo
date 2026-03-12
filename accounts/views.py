from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages

from .forms import CadastroBasicoForm, UserProfileForm
from .models import UserProfile
from library.models import LibraryItem
from forum.models import Topico, Resposta

class SignupView(CreateView):
    form_class = CadastroBasicoForm
    template_name = 'registration/signup.html'
    
    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('complete_profile')

class CompleteProfileView(LoginRequiredMixin, UpdateView):
    model = UserProfile
    form_class = UserProfileForm
    template_name = 'registration/complete_profile.html'

    def get_object(self):
        return self.request.user.profile

    def get_success_url(self):
        messages.success(self.request, 'Perfil atualizado com sucesso!')
        return reverse_lazy('perfil_usuario', kwargs={'slug': self.object.slug})



def perfil_usuario(request, slug):
    request.session['ultimo_contexto'] = 'perfil'
    
    perfil = get_object_or_404(UserProfile, slug=slug)
    user_perfil = perfil.user
    
    is_dono = (request.user == user_perfil)
    
    itens_acervo = LibraryItem.objects.filter(usuario_criador=user_perfil).order_by('-criado_em')
    if not is_dono:
        itens_acervo = itens_acervo.filter(status='ATIVO')
        
    topicos = Topico.objects.filter(autor=user_perfil, ativa=True).order_by('-data_criacao')
    respostas = Resposta.objects.filter(autor=user_perfil).order_by('-data_postagem')
    
    if not is_dono:
        topicos = topicos.filter(status='APROVADO')
    
    contexto = {
        'user_perfil': user_perfil,
        'perfil': perfil,
        'is_dono': is_dono,
        'itens_acervo': itens_acervo,
        'topicos': topicos,
        'respostas': respostas,
    }
    
    return render(request, 'accounts/perfil.html', contexto)