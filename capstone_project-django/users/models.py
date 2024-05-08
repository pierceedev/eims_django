from django.db import models
from django.contrib.auth.models import AbstractUser
from rooms.models import Department
    
class User(AbstractUser):
    is_superuser = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_secretary = models.BooleanField(default=False)
    is_dean = models.BooleanField(default=False)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, blank=True, null=True)
    contact_number = models.CharField(max_length=20, blank=True, null=True)
    
        
    def user_type(self):
        if self.is_admin:
            return "Admin"
        elif self.is_secretary:
            return "Secretary"
        elif self.is_dean:
            return "Dean"
        elif self.is_superuser:
            return "Superuser"
        else:
            return "Staff"

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.user_type()})"