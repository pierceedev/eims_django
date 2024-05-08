from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.views import generic
from django.urls import reverse_lazy
from django.core.mail import send_mail
from django.contrib.auth.mixins import LoginRequiredMixin
from users.mixins import StaffRequiredMixin, AdminRequiredMixin
from django.contrib.auth import get_user_model
from .forms import StaffModelForm, StaffUpdateForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

User = get_user_model()



class MyView(StaffRequiredMixin, generic.View):
    pass

class StaffListView(AdminRequiredMixin, generic.ListView):
    template_name = 'staffs/staff_list.html'
    model = User

    def get_queryset(self):
        return User.objects.filter(is_staff=True, is_secretary=False, is_dean=False)
    


class StaffCreateView(AdminRequiredMixin, generic.CreateView):
    form_class = StaffModelForm
    template_name = 'staffs/staff_create.html'
    success_url = reverse_lazy('staffs:staff-list')

    def form_valid(self, form):
    # Save the user
        user = form.save(commit=False)
        user.set_password(form.cleaned_data['password'])  # Hash the password
        user.is_staff = True
        user.save()

    # Send invitation email
        subject = "EIMS Capstone Invitation"
        message = "You are invited to be a Staff in EIMS Capstone"
        from_email = "eims@test.com"
        recipient_list = [user.email]
        send_mail(subject, message, from_email, recipient_list)

        return super().form_valid(form)


class StaffDetailView(AdminRequiredMixin,  generic.DetailView):
    template_name = 'staffs/staff_detail.html'
    context_object_name = 'staff'   
    
    def get_queryset(self):
        return User.objects.all()
    
class StaffUpdateView(AdminRequiredMixin, generic.UpdateView):
    model = User
    form_class = StaffUpdateForm
    template_name = 'staffs/staff_update.html'
    success_url = reverse_lazy('staffs:staff-list')

    def form_valid(self, form):
        messages.info(self.request, "You have successfully updated this User.")
        return super().form_valid(form)

