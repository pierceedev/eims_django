from django.urls import path
from . views import (
    ItemListView, ItemCreateView, ItemDetailView, ItemUpdateView, ItemDeleteView, 
    DashboardView, ItemBorrowView,  BorrowItemListView, AddUserView, ReturnItemView, ReturnedItemListView
    
)
from . import views

app_name = 'secretary'

urlpatterns = [
    path('', ItemListView.as_view(), name='item-list'),
    path('new/', ItemCreateView.as_view(), name='item-new'),
    path('<int:pk>/', ItemDetailView.as_view(), name='item-detail'),
    path('<int:pk>/update/', ItemUpdateView.as_view(), name='item-update'),
    path('<int:pk>/delete/', ItemDeleteView.as_view(), name='item-delete'),
    path('dashboard/', DashboardView.as_view(), name='item-dashboard'),
    path('borrow/', ItemBorrowView.as_view(), name='item-borrow'),
    path('borrowed/', BorrowItemListView.as_view(), name='borrowed-list'),
    path('return-item/<int:pk>/', ReturnItemView.as_view(), name='return-item'),
    path('returned-item/', ReturnedItemListView.as_view(), name='returned-list'),
    path('add user/', AddUserView.as_view(), name='add-user'),


]