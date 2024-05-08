from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()

class StaffModelForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'department',
            'email',
            'contact_number',
            'password',

        ]

class StaffUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'department',
            'email',
            'contact_number',
        ]