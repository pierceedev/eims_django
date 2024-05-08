from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import AbstractUser
from django.dispatch import receiver
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.utils.dateformat import format
import uuid

from rooms.models import Room



User = get_user_model()

class Equipment(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(blank=True, null=True, max_length=1000)
    price = models.IntegerField(blank=True, null=True)
    quantity = models.IntegerField(default=1, blank=True, null=True)

    def __str__(self):
        return f"{self.name}"
    
class BorrowedEquipment(models.Model):
    borrower = models.ForeignKey(User, on_delete=models.CASCADE)
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    date_borrowed = models.DateTimeField(auto_now_add=True)
    
    def return_equipment(self):

        # Add the quantity back to the equipment
        
        self.equipment.quantity += self.quantity  
        self.equipment.save()
        self.delete()

    def __str__(self):
        formatted_date = format(self.date_borrowed, 'N j, Y, P')
        return f"{formatted_date} - {self.borrower.first_name} {self.borrower.last_name} borrowed {self.equipment.description} of  {self.quantity} of {self.equipment.name} at {self.room.name} "


