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
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError
from allauth.account.models import EmailAddress

class SignupView(CreateView):
    form_class = CadastroBasicoForm
    template_name = 'registration/signup.html'
    
    def form_valid(self, form):
        user = form.save()        
        EmailAddress.objects.get_or_create(
            user=user, 
            email=user.email,
            defaults={'primary': True, 'verified': False}
        )
        
        self.request.session['registro_usuario_id'] = user.id
        return redirect('complete_profile')

class CompleteProfileView(UpdateView):
    model = UserProfile
    form_class = UserProfileForm
    template_name = 'registration/complete_profile.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated: return redirect('home')
        if not request.session.get('registro_usuario_id'): return redirect('signup')
        return super().dispatch(request, *args, **kwargs)

    def get_object(self):
        user_id = self.request.session.get('registro_usuario_id')
        return get_object_or_404(UserProfile, user__id=user_id)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['base_template'] = 'base_auth.html'
        user_id = self.request.session.get('registro_usuario_id')
        ctx['usuario_registro'] = get_object_or_404(User, id=user_id)
        return ctx

    def post(self, request, *args, **kwargs):
        if 'pular' in request.POST:
            user_id = self.request.session.get('registro_usuario_id')
            user = get_object_or_404(User, id=user_id)
            
            email_obj = EmailAddress.objects.get(user=user, primary=True)
            email_obj.send_confirmation(self.request, signup=True)

            if 'registro_usuario_id' in self.request.session:
                del self.request.session['registro_usuario_id']
                
            messages.info(self.request, 'Cadastro adiado! Enviamos um link de ativação para o seu e-mail. Verifique sua caixa de entrada para fazer o login.')
            return redirect(self.get_success_url())
            
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        response = super().form_valid(form)
        user_id = self.request.session.get('registro_usuario_id')
        user = get_object_or_404(User, id=user_id)
        
        email_obj = EmailAddress.objects.get(user=user, primary=True)
        email_obj.send_confirmation(self.request, signup=True)

        if 'registro_usuario_id' in self.request.session:
            del self.request.session['registro_usuario_id']
            
        messages.success(self.request, 'Perfil criado! Agora, acesse seu e-mail para ativar sua conta antes de fazer o login.')
        return response

    def get_success_url(self):
        return reverse_lazy('login')

class EditProfileView(LoginRequiredMixin, UpdateView):
        model = UserProfile
        form_class = UserProfileForm
        template_name = 'registration/complete_profile.html'

        def get_object(self):
            return self.request.user.profile

        def get_context_data(self, **kwargs):
            ctx = super().get_context_data(**kwargs)
            ctx['base_template'] = 'base.html'
            ctx['usuario_registro'] = self.request.user
            return ctx

        def form_valid(self, form):
            messages.success(self.request, 'Perfil atualizado com sucesso!')
            return super().form_valid(form)

        def get_success_url(self):
            return reverse_lazy('perfil_usuario', kwargs={'username': self.request.user.username})

def perfil_usuario(request, username):
    request.session['ultimo_contexto'] = 'perfil'
    user_perfil = get_object_or_404(User, username=username)
    perfil = user_perfil.profile
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
                request.session['acessibilidade'] = dados
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
    
class CustomAuthForm(AuthenticationForm):
    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        if username and password:
            try:
                user = User.objects.get(username=username)            
                if user.check_password(password):
                    if not user.is_active:
                        raise ValidationError("Sua conta foi banida.", code='inactive')
                    
                    email_verified = EmailAddress.objects.filter(user=user, verified=True).exists()
                    if not email_verified:
                        raise ValidationError("Você precisa confirmar seu e-mail antes de entrar! Verifique sua caixa de entrada.", code='email_unverified')
            except User.DoesNotExist:
                pass          
        return super().clean()

class CustomLoginView(LoginView):
    form_class = CustomAuthForm
    template_name = 'registration/login.html'