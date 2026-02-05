from django.contrib import admin
from .models import Booking, Payment , ManagerBooking , GuestBooking

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['reservation_number', 'guest', 'room', 'status', 'check_in_date', 'check_out_date', 'total_price']
    list_filter = ['status', 'check_in_date']
    search_fields = ['reservation_number', 'guest__username']


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['transaction_id', 'reservation', 'amount', 'payment_status', 'payment_method']
    list_filter = ['payment_status', 'payment_method']


from django.contrib import admin
from .models import Booking, Payment, ManagerBooking, GuestBooking


class BaseBookingAdmin(admin.ModelAdmin):
    list_display = (
        'reservation_number',
        'guest',
        'room',
        'status',
        'check_in_date',
        'check_out_date',
        'total_price',
    )
    list_filter = ('status', 'check_in_date', 'check_out_date')
    search_fields = ('reservation_number', 'guest__username', 'room__number')
    readonly_fields = ('reservation_number', 'total_price', 'created_at', 'updated_at')
    ordering = ('-created_at',)

    fieldsets = (
        ('Booking Info', {
            'fields': (
                'reservation_number',
                'guest',
                'room',
                'status',
            )
        }),
        ('Dates', {
            'fields': (
                'check_in_date',
                'check_out_date',
                'number_of_guests',
            )
        }),
        ('Price & Notes', {
            'fields': (
                'total_price',
                'special_requests',
            )
        }),
        ('Check In / Out', {
            'fields': (
                'checked_in_by',
                'checked_out_by',
            )
        }),
        ('System Info', {
            'fields': (
                'created_at',
                'updated_at',
            )
        }),
    )

    
@admin.register(ManagerBooking)
class ManagerBookingAdmin(BaseBookingAdmin):
    actions = ['confirm_booking', 'cancel_booking', 'check_in', 'check_out']

    def confirm_booking(self, request, queryset):
        queryset.update(status='confirmed')
    confirm_booking.short_description = "Confirm selected bookings"

    def cancel_booking(self, request, queryset):
        queryset.update(status='cancelled')
    cancel_booking.short_description = "Cancel selected bookings"

    def check_in(self, request, queryset):
        queryset.update(
            status='checked_in',
            checked_in_by=request.user
        )
    check_in.short_description = "Check in guests"

    def check_out(self, request, queryset):
        queryset.update(
            status='checked_out',
            checked_out_by=request.user
        )
    check_out.short_description = "Check out guests"
