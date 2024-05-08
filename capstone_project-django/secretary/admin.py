from django.contrib import admin
from .models import Item,  User, BorrowedItem, ReturnItemHistory

admin.site.register(Item)
admin.site.register(User)
admin.site.register(ReturnItemHistory)
admin.site.register(BorrowedItem)