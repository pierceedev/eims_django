from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse_lazy
from django.views import generic
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from users.mixins import DeanRequiredMixin
from .models import Equipment, BorrowedEquipment
from .forms import EquipmentSearchForm, EquipmentForm, BorrowEquipmentForm




class EquipmentListView(DeanRequiredMixin, generic.ListView):
    template_name = 'rlab/eq_list.html'
    queryset = Equipment.objects.all()
    form_class = EquipmentSearchForm  # Assign the form class to the view

    def get_queryset(self):
        queryset = super().get_queryset()  # Retrieve the original queryset

        # Check if a search term was submitted
        search_term = self.request.GET.get('search_term')
        if search_term:
            queryset = queryset.filter(name__icontains=search_term)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.form_class()  # Instantiate the form
        return context

class BorrowEquipmentListView(LoginRequiredMixin, generic.ListView):
    template_name = 'rlab/borrowed_list.html'
    

    def get_queryset(self):
        queryset = BorrowedEquipment.objects.all()
        if self.request.user.is_staff:
            return queryset.filter(borrower=self.request.user)
        return queryset

class EquipmentDetailView(DeanRequiredMixin, generic.DetailView):
    model = Equipment
    template_name = 'rlab/eq_detail.html'

class EquipmentCreateView(DeanRequiredMixin, generic.CreateView):
    template_name = 'rlab/eq_create.html'
    form_class = EquipmentForm
    success_url = reverse_lazy("rlab:equipment-list")

    def form_valid(self, form):
        messages.success(self.request, 'Equipment Added Successfully!')
        return super().form_valid(form)


class EquipmentUpdateView(DeanRequiredMixin, generic.UpdateView):
    model = Equipment
    form_class = EquipmentForm
    template_name = 'rlab/eq_update.html'
    success_url = reverse_lazy('rlab:equipment-list')

    def form_valid(self, form):
        messages.info(self.request, "You have successfully updated this Equipment.")
        return super().form_valid(form)
    
class EquipmentDeleteView(DeanRequiredMixin, generic.DeleteView):
    template_name = 'rlab/eq_delete.html'
    model = Equipment
    success_url = reverse_lazy("rlab:equipment-list")

class EquipmentBorrowView(DeanRequiredMixin, generic.CreateView):
    template_name = 'rlab/eq_borrow.html'
    form_class = BorrowEquipmentForm
    success_url = reverse_lazy('rlab:eq-borrowed-list')

    def form_valid(self, form):
        # Deduct the quantity from the item
        equipment = form.cleaned_data['equipment']
        quantity_borrowed = form.cleaned_data['quantity']

        if quantity_borrowed <= equipment.quantity:
            equipment.quantity -= quantity_borrowed
            equipment.save()

            # Save the borrowed item
            form.save()
            messages.success(self.request, 'Item borrowed successfully.')
            return super().form_valid(form)
        else:
            messages.error(self.request, 'Not enough quantity available.')
            return redirect('rlab:equipment-list')
        
class ReturnEquipmentView(DeanRequiredMixin, generic.RedirectView):
    permanent = False
    query_string = True
    pattern_name = 'eq-borrowed-list'
    

    def get(self, request, *args, **kwargs):
        borrowed_equipment = get_object_or_404(BorrowedEquipment, pk=kwargs['pk'])
        borrowed_equipment.return_equipment()
        messages.success(request, 'Item returned successfully.')
        success_url = reverse_lazy(self.pattern_name)
        return redirect('rlab:eq-borrowed-list')

