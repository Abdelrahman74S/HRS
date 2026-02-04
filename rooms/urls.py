from django.urls import path
from .views import (
    RoomListView,
    RoomCreateView,
    RoomUpdateView,
    RoomDetailView,
    RoomDeleteView,
    search,
)

app_name ='rooms'

urlpatterns = [
    path('', RoomListView.as_view(), name='room_list'),

    path('create/', RoomCreateView.as_view(), name='room_create'),

    path('search/', search, name='room_search'),
    path('<slug:slug>/', RoomDetailView.as_view(), name='room_detail'),

    path('<slug:slug>/update/', RoomUpdateView.as_view(), name='room_update'),

    path('<slug:slug>/delete/', RoomDeleteView.as_view(), name='room_delete'),

]
