from django.shortcuts import reverse
from django.urls import reverse_lazy
from django.views.generic.base import TemplateView
from django.views.generic.edit import UpdateView, CreateView
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import RegistrationForm, ProfileChangeForm


class HomeView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/home.html'
    login_url = reverse_lazy('datasets:list')


class RegisterView(CreateView):
    template_name = 'accounts/reg_form.html'
    form_class = RegistrationForm

    def get_success_url(self):
        return reverse('accounts:home')


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/view_profile.html'
    login_url = reverse_lazy('accounts:login')

    def get_context_data(self):
        context = super().get_context_data()
        context['user'] = self.request.user
        return context


class EditProfileView(LoginRequiredMixin, UpdateView):
    form_class = ProfileChangeForm
    template_name = 'accounts/edit_profile.html'
    success_url = reverse_lazy('accounts:view_profile')
    login_url = reverse_lazy('accounts:view_profile')

    def get_object(self):
        return self.request.user


class ProfilePasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    template_name = 'accounts/change_password.html'
    success_url = reverse_lazy('accounts:profile')
    login_url = reverse_lazy('accounts:login')
