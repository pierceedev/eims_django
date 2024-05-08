from django.urls import path
from . views import (
    
    RoomListView, RoomCreateView, RoomDetailView, RoomUpdateView, RoomDeleteView
)

app_name = 'rooms'

urlpatterns = [
    path('', RoomListView.as_view(), name='room-list'),
    path('room/add/', RoomCreateView.as_view(), name='room-new'),
    path('room/<int:pk>/', RoomDetailView.as_view(), name='room-detail'),
    path('room/<int:pk>/update/', RoomUpdateView.as_view(), name='room-update'),
    path('room/<int:pk>/delete/', RoomDeleteView.as_view(), name='room-delete'),
]