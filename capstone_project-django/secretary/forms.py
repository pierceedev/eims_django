from django import forms
from .models import Item, BorrowedItem
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

User = get_user_model()

class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['name', 'description', 'price', 'quantity', 'batch_id']

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if not name:
            raise forms.ValidationError("Please enter an item name.")
        return name
    
    def clean_price(self):
        price = self.cleaned_data.get('price')
        if not price:
            raise forms.ValidationError("Please enter a price.")
        return price

    def clean_batch_id(self):
        batch_id = self.cleaned_data.get('batch_id')
        if not batch_id:
            raise forms.ValidationError("Please enter a batch ID.")
        return batch_id

class ItemUpdateForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['name', 'category', 'description', 'price', 'quantity', 'batch_id']
        
class ItemSearchForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['name', 'description', 'price', 'quantity', 'batch_id']


class BorrowItemForm(forms.ModelForm):
    class Meta:
        model = BorrowedItem
        fields = ['borrower', 'item', 'quantity']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['borrower'].queryset = User.objects.filter(is_staff=True, is_superuser=False, is_active=True)
        self.fields['item'].queryset = Item.objects.exclude(quantity=0)
        
    def clean_borrower(self):
        borrower = self.cleaned_data.get('borrower')
        if not borrower:
            raise forms.ValidationError("Only secretaries can borrow items.")
        return borrower
    
    def clean_item(self):
        item = self.cleaned_data.get('item')
        if not item:
            raise forms.ValidationError("Please select an item to borrow.")
        return item

class  UserCreateForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']
        

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_secretary = self.cleaned_data['is_secretary']
        user.is_dean = self.cleaned_data['is_dean']
        user.is_staff = self.cleaned_data['is_staff']
        if commit:
            user.save()
        return user