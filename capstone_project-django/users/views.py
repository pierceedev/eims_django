from django.contrib import messages
from django.conf import settings
from django.shortcuts import get_object_or_404, render , redirect
from django.contrib.auth.views import LoginView as AuthLoginView
from django.contrib.auth import authenticate, login as auth_login, logout
from django.urls import reverse_lazy
from django.utils import timezone
from django.http import HttpResponse
from django.views import generic
from users.mixins import AdminRequiredMixin
from django.core.mail import send_mail
from .models import User
from .forms import UserModelForm, UserUpdateForm


class LoginView(AuthLoginView):
    template_name = 'users/login.html'
    
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            user = request.user
            if user.is_superuser:
                return redirect ("admin/")
            elif user.is_secretary:
                return redirect ("profile/")
            else:
                return redirect ("home/")
        else:
            return super().get(request, *args, **kwargs)
        
class LogoutView(AuthLoginView):
    url = reverse_lazy('login')

    def get(self, request, *args, **kwargs):
        logout(request)
        if not request.user.is_authenticated:
            return redirect('login')
        else:
            return super().get(request, *args, **kwargs)
        

class UserListView(AdminRequiredMixin, generic.ListView):
    model = User
    template_name = 'users/user_list.html'

    def get_queryset(self):
        return User.objects.all()

class UserCreateView(AdminRequiredMixin, generic.CreateView):
    form_class = UserModelForm
    template_name = 'users/new_user.html'
    success_url = reverse_lazy('users:user-list')

    def form_valid(self, form):
    # Save the user
        user = form.save(commit=False)
        user.set_password(form.cleaned_data['password'])  # Hash the password
        user.save()

    # Send invitation email
        subject = "EIMS Capstone Invitation"
        message = "You are invited to be a Staff in EIMS Capstone"
        from_email = "eims@test.com"
        recipient_list = [user.email]
        send_mail(subject, message, from_email, recipient_list)

        return super().form_valid(form)

class UserUpdateView(AdminRequiredMixin, generic.UpdateView):
    model = User
    form_class = UserUpdateForm
    template_name = 'users/user_update.html'
    success_url = reverse_lazy('users:user-list')

    def form_valid(self, form):
        messages.info(self.request, "You have successfully updated this User.")
        return super().form_valid(form)



        




