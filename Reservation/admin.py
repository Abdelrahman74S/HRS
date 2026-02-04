from django.contrib import admin
from .models import Booking, Payment

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['reservation_number', 'guest', 'room', 'status', 'check_in_date', 'check_out_date', 'total_price']
    list_filter = ['status', 'check_in_date']
    search_fields = ['reservation_number', 'guest__username']

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['transaction_id', 'reservation', 'amount', 'payment_status', 'payment_method']
    list_filter = ['payment_status', 'payment_method']