from django.urls import path
from . views import (
    EquipmentListView, EquipmentCreateView, EquipmentDetailView, EquipmentUpdateView, EquipmentDeleteView, EquipmentBorrowView,
    BorrowEquipmentListView, ReturnEquipmentView
    
)

app_name = 'rlab'

urlpatterns = [
    
    path('', EquipmentListView.as_view(), name='equipment-list'),
    path('new/', EquipmentCreateView.as_view(), name='equipment-new'),
    path('<int:pk>/', EquipmentDetailView.as_view(), name='equipment-detail'),
    path('<int:pk>/update/', EquipmentUpdateView.as_view(), name='equipment-update'),
    path('<int:pk>/delete/', EquipmentDeleteView.as_view(), name='equipment-delete'),
    path('borrow/', EquipmentBorrowView.as_view(), name='equipment-borrow'),
    path('borrowed/', BorrowEquipmentListView.as_view(), name='eq-borrowed-list'),
    path('return-equipment/<int:pk>/', ReturnEquipmentView.as_view(), name='return-equipment'),
]