from django import forms
from .models import Equipment, BorrowedEquipment
from users.models import User




class EquipmentForm(forms.ModelForm):
    class Meta:
        model = Equipment
        fields = ['name', 'description', 'price', 'quantity']



class EquipmentSearchForm(forms.ModelForm):
    class Meta:
        model = Equipment
        fields = ['name', 'description', 'price', 'quantity']




class BorrowEquipmentForm(forms.ModelForm):
    class Meta:
        model = BorrowedEquipment
        fields = ['borrower', 'equipment', 'quantity', 'room']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['borrower'].queryset = User.objects.filter(is_staff=True)
        self.fields['equipment'].queryset = Equipment.objects.exclude(quantity=0)
        