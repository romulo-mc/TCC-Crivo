from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import CadastroBasicoForm, UserProfileForm
from .models import UserProfile

class SignupView(CreateView):
    form_class = CadastroBasicoForm
    template_name = 'registration/signup.html'
    
    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('complete_profile')

class CompleteProfileView(LoginRequiredMixin, CreateView):
    model = UserProfile
    form_class = UserProfileForm
    template_name = 'registration/complete_profile.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)