from django.shortcuts import render , redirect
from .forms import UserForm , UserRegisterForm
from .models import User
from django.contrib.auth.views import LoginView 
from django.views.generic  import CreateView, DetailView ,UpdateView
from django.contrib.auth import  login , logout 
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.views.generic import TemplateView
# Create your views here.

class UserRegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('rooms:room_list')

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        return response


class UserLoginView(LoginView):
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True
    success_url = reverse_lazy('rooms:room_list')

@login_required
def LogoutView(request):
    logout(request)
    return redirect('accounts:login')

class UserProfileView(LoginRequiredMixin,DetailView):
    model = User 
    template_name = 'accounts/profile.html'
    context_object_name = 'user_profile' 
    
    def get_object(self): 
        return self.request.user

class UserProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserForm
    template_name = 'accounts/profile_update.html'
    success_url = reverse_lazy('accounts:profile')

    def get_object(self):
        return self.request.user

    


class ChangePasswordView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/change_password.html'

    def post(self, request, *args, **kwargs):
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            return redirect('accounts:profile')
        return render(request, self.template_name, {'form': form})
