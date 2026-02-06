from django.urls import path
from . import views

app_name = 'reservations'

urlpatterns = [
    path('book/<slug:room_slug>/', views.BookingCreateView.as_view(), name='book_room'),
    
    path('my-bookings/', views.UserBookingListView.as_view(), name='my_bookings'),
    
    path('<int:pk>/', views.BookingDetailView.as_view(), name='booking_detail'),
    
    path('<int:pk>/cancel/', views.BookingDeleteView.as_view(), name='booking_delete'),

    path('pay/<int:booking_id>/', views.CreatePaymentView.as_view(), name='process_payment'),
    
    path('check-in/<int:booking_id>/', views.check_in_guest, name='check_in'),
    
    path('check-out/<int:booking_id>/', views.check_out_guest, name='check_out'),
]