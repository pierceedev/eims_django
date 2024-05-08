from django.urls import path
from . views import (
    StaffListView, StaffDetailView, StaffCreateView, StaffUpdateView
)
app_name = 'staffs'

urlpatterns = [

        path('', StaffListView.as_view(), name='staff-list'),
        path('<int:pk>/', StaffDetailView.as_view(), name='staff-detail'),
        path('<int:pk>/update/', StaffUpdateView.as_view(), name='staff-update'),
        path('add/', StaffCreateView.as_view(), name='staff-create'),
]

