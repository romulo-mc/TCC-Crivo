from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.views import View
from django.contrib.auth.models import User
from .forms import CadastroBasicoForm, UserProfileForm, AcessibilidadeForm, ConfiguracoesForm
from .models import UserProfile
from library.models import LibraryItem
from forum.models import Topico, Resposta

class SignupView(CreateView):
    form_class = CadastroBasicoForm
    template_name = 'registration/signup.html'
    
    def form_valid(self, form):
        user = form.save()
        self.request.session['registro_usuario_id'] = user.id
        return redirect('complete_profile')

class CompleteProfileView(UpdateView):
    model = UserProfile
    form_class = UserProfileForm
    template_name = 'registration/complete_profile.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated and not request.session.get('registro_usuario_id'):
            return redirect('signup')
        return super().dispatch(request, *args, **kwargs)

    def get_object(self):
        if self.request.user.is_authenticated:
            return self.request.user.profile
        
        user_id = self.request.session.get('registro_usuario_id')
        return get_object_or_404(UserProfile, user__id=user_id)

    def form_valid(self, form):
        response = super().form_valid(form)
        
        if not self.request.user.is_authenticated:
            user_id = self.request.session.get('registro_usuario_id')
            user = get_object_or_404(User, id=user_id)
            login(self.request, user)
            
            if 'registro_usuario_id' in self.request.session:
                del self.request.session['registro_usuario_id']
                
            messages.success(self.request, 'Conta criada com sucesso! Bem-vindo(a) ao Crivo!')
        else:
            messages.success(self.request, 'Perfil atualizado com sucesso!')
            
        return response

    def get_success_url(self):
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


class AcessibilidadeView(View):
    def get(self, request):
        if request.user.is_authenticated:
            form = AcessibilidadeForm(instance=request.user.profile)
        else:
            initial_data = request.session.get('acessibilidade', {})
            form = AcessibilidadeForm(initial=initial_data)
        return render(request, 'accounts/acessibilidade.html', {'form': form})

    def post(self, request):
        if request.user.is_authenticated:
            form = AcessibilidadeForm(request.POST, instance=request.user.profile)
        else:
            form = AcessibilidadeForm(request.POST)

        if form.is_valid():
            if request.user.is_authenticated:
                form.save()
            else:
                dados = form.cleaned_data
                request.session['acessibilidade'] = {
                    'modo_escuro': dados.get('modo_escuro', False),
                    'alto_contraste': dados.get('alto_contraste', False),
                    'fonte_dislexia': dados.get('fonte_dislexia', False),
                    'fonte_tdah': dados.get('fonte_tdah', False),
                    'reduzir_animacoes': dados.get('reduzir_animacoes', False),
                    'tamanho_fonte': dados.get('tamanho_fonte', 'M'),
                }

            messages.success(request, 'Preferências de acessibilidade atualizadas!')
            return redirect('acessibilidade')
        return render(request, 'accounts/acessibilidade.html', {'form': form})


class ConfiguracoesView(LoginRequiredMixin, UpdateView):
    model = UserProfile
    form_class = ConfiguracoesForm
    template_name = 'accounts/configuracoes.html'

    def get_object(self):
        return self.request.user.profile

    def get_success_url(self):
        messages.success(self.request, 'Configurações salvas com sucesso!')
        return reverse_lazy('configuracoes')