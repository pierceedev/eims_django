from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.http import HttpResponse
from django.views import generic
from django.urls import reverse_lazy
from .models import Item, User, BorrowedItem, ReturnItemHistory
from .forms import ItemForm, BorrowItemForm, UserCreateForm, ItemSearchForm, ItemUpdateForm
from django.contrib.auth.mixins import LoginRequiredMixin
from users.mixins import DeanRequiredMixin, StaffRequiredMixin, SecretaryRequiredMixin
import barcode
from barcode.writer import ImageWriter
import tempfile
import os
import qrcode
from django.conf import settings



class LandingPageView(generic.TemplateView):
    template_name = 'landing_page.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("profile")
        return super().dispatch(request, *args, **kwargs)
    
class ProfileView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add context data here
        context['user'] = self.request.user  # For example, adding the logged-in user object to the context
        return context

class ExportCSVView(generic.View):
    def get(self, request, *args, **kwargs):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="Items.csv"'

        writer = csv.writer(response)
        writer.writerow(['Column 1', 'Column 2', 'Column 3'])  # Add column headers

        queryset = Item.objects.all()  # Retrieve data from your model
        for obj in queryset:
            writer.writerow([obj.name, obj.description, obj.quantity, obj.price])  # Add data rows

        return response
class DashboardView(StaffRequiredMixin, generic.TemplateView):
    template_name = 'secretary/dashboard.html'

class ItemListView(SecretaryRequiredMixin, generic.ListView):
    template_name = 'secretary/item_list.html'
    queryset = Item.objects.all()
    form_class = ItemSearchForm  # Assign the form class to the view

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

class BorrowItemListView(SecretaryRequiredMixin, generic.ListView):
    template_name = 'secretary/borrowed_list.html'
    queryset = BorrowedItem.objects.all()

class ItemDetailView(SecretaryRequiredMixin, generic.DetailView):
    model = Item
    template_name = 'secretary/item_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        item = self.get_object()
        batch_items = Item.objects.filter(batch_id=item.batch_id)
        context['batch_items'] = batch_items
        return context
    
class ItemCreateView(SecretaryRequiredMixin, generic.CreateView):
    template_name = 'secretary/item_create.html'
    form_class = ItemForm
    success_url = reverse_lazy("secretary:item-list")

    
class ItemUpdateView(SecretaryRequiredMixin, generic.UpdateView):

    model = Item
    form_class = ItemUpdateForm
    template_name = 'secretary/item_update.html'
    success_url = reverse_lazy('secretary:item-list')

    def form_valid(self, form):
        messages.info(self.request, "You have successfully updated this item")
        return super().form_valid(form)


class ItemDeleteView(SecretaryRequiredMixin, generic.DeleteView):
    template_name = 'secretary/item_delete.html'
    model = Item
    success_url = reverse_lazy("secretary:item-list")

class ItemBorrowView(SecretaryRequiredMixin, generic.CreateView):
    template_name = 'secretary/item_borrow.html'
    form_class = BorrowItemForm
    success_url = reverse_lazy('secretary:borrowed-list')

    def form_valid(self, form):
        # Deduct the quantity from the item
        item = form.cleaned_data['item']
        quantity_borrowed = form.cleaned_data['quantity']

        if quantity_borrowed <= item.quantity:
            item.quantity -= quantity_borrowed
            item.save()

            # Save the borrowed item
            form.save()
            messages.success(self.request, 'Item borrowed successfully.')
            return super().form_valid(form)
        else:
            messages.error(self.request, 'Not enough quantity available.')
            return redirect('secretary:item-borrow')
        
class ReturnItemView(SecretaryRequiredMixin, generic.RedirectView):
        def get(self, request, *args, **kwargs):
            borrowed_item = get_object_or_404(BorrowedItem, pk=kwargs['pk'])
            borrower = borrowed_item.borrower
            returned_item = borrowed_item.item
            borrowed_item.return_item()
            ReturnItemHistory.objects.create(item=returned_item, borrower=borrower)
            messages.success(request, 'Item returned successfully.')
            return redirect('secretary:borrowed-list')
        
class ReturnedItemListView(SecretaryRequiredMixin, generic.ListView):
    template_name = 'secretary/return_history.html'
    queryset = ReturnItemHistory.objects.all()


    
class AddUserView(SecretaryRequiredMixin, generic.CreateView):
    template_name = 'secretary/add_user.html'
    form_class = UserCreateForm
    success_url = reverse_lazy("secretary:add-user")

