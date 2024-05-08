from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()

class UserModelForm(forms.ModelForm):
    # Define a field for user_type as a ChoiceField
    

    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'password',
            'department',
            'contact_number',
            'is_admin',
            'is_secretary',
            'is_dean',
        ]

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'department',
            'contact_number',
            'is_active',
            'is_admin',
            'is_secretary',
            'is_dean',
        ]