from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import AbstractUser
from django.dispatch import receiver
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.utils.dateformat import format
import uuid


User = get_user_model()


class Category(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.name}"
    
class Item(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True)
    description = models.TextField(blank=True, null=True, max_length=1000)
    price = models.IntegerField(blank=True, null=True)
    quantity = models.IntegerField(default=1, blank=True, null=True)
    batch_id = models.CharField(max_length=50, blank=True, null=True)
    unique_identifier = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)  # Unique identifier field

    def save(self, *args, **kwargs):
        # Generate batch_id if not provided
        if not self.batch_id:
            self.batch_id = uuid.uuid4().hex  # Generate a unique batch ID using UUID
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name}"
    
class BorrowedItem(models.Model):
    borrower = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    date_borrowed = models.DateTimeField(auto_now_add=True)
    
    def return_item(self):

        # Add the quantity back to the item
        
        self.item.quantity += self.quantity  
        self.item.save()
        self.delete()

    def __str__(self):
        formatted_date = format(self.date_borrowed, 'N j, Y, P')
        return f"{self.borrower.username} borrowed {self.item.description} of  {self.quantity} of {self.item.name} on {formatted_date}"

class ReturnItemHistory(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    borrower = models.ForeignKey(User, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1, blank=True, null=True)
    date_returned = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        formatted_date = format(self.date_returned, 'N j, Y, P')
        return f"{self.item.name} by {self.borrower.username} was returned on {formatted_date}"
    