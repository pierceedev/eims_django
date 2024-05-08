from django.shortcuts import render
from django.views import generic
from django.urls import reverse_lazy
from users.mixins import DeanRequiredMixin, StaffRequiredMixin, SecretaryRequiredMixin, AdminRequiredMixin
from .models import Room
from .forms import RoomForm

# Create your views here.
class RoomListView(AdminRequiredMixin, generic.ListView):
    template_name = 'rooms/room_list.html'
    queryset = Room.objects.all()

class RoomDetailView(AdminRequiredMixin, generic.DetailView):
    template_name = 'rooms/room_detail.html'
    queryset = Room.objects.all()

class RoomCreateView(AdminRequiredMixin, generic.CreateView):
    template_name = 'rooms/room_create.html'
    form_class = RoomForm
    success_url = reverse_lazy("rooms:room-list")

class RoomUpdateView(AdminRequiredMixin, generic.UpdateView):
    template_name = 'rooms/room_update.html'
    form_class = RoomForm
    queryset = Room.objects.all()
    success_url = reverse_lazy("rooms:room-list")

class RoomDeleteView(AdminRequiredMixin, generic.DeleteView):
    template_name = 'rooms/room_delete.html'
    model = Room
    success_url = reverse_lazy("rooms:room-list")