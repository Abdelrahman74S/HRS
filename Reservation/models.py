import uuid
from django.db import models
from accounts.models import User
from rooms.models import Room

class Booking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('checked_in', 'Checked In'),
        ('checked_out', 'Checked Out'),
        ('cancelled', 'Cancelled'),
    ]

    reservation_number = models.CharField(max_length=10, unique=True, editable=False)
    guest = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='reservations')
    
    check_in_date = models.DateField()
    check_out_date = models.DateField()
    number_of_guests = models.PositiveIntegerField(default=1)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    special_requests = models.TextField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    checked_in_by = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='checkins_handled'
    )
    checked_out_by = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='checkouts_handled'
    )

    def sum_total_price(self):
        base = self.room.room_type.base_price 
        
        extra = self.room.pricing_override or 0
        
        single_night_price = base + extra
    
        if self.check_out_date and self.check_in_date:
            nights = (self.check_out_date - self.check_in_date).days
            nights = max(nights, 1) 
            self.total_price = single_night_price * nights
        else:
            self.total_price = single_night_price
    
        return self.total_price

    def save(self, *args, **kwargs):
        if not self.reservation_number:
            self.reservation_number = self.generate_reservation_number()
            
        self.sum_total_price()
        
        super().save(*args, **kwargs)

    def generate_reservation_number(self):
        return uuid.uuid4().hex[:10].upper()

    def __str__(self):
        return f"Booking {self.reservation_number} - {self.guest.username}"

    class Meta:
        ordering = ['-created_at']
        

class Payment(models.Model):
    METHOD_CHOICES = [
        ('credit_card', 'Credit Card'),
        ('cash', 'Cash'),
        ('bank_transfer', 'Bank Transfer'),
    ]

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('refunded', 'Refunded'),
    ]

    reservation = models.OneToOneField(
        Booking, 
        on_delete=models.CASCADE, 
        related_name='payment'
    )

    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=20, choices=METHOD_CHOICES)
    payment_status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='pending'
    )
    
    transaction_id = models.CharField(max_length=100, unique=True, blank=True, null=True)
    
    payment_date = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment {self.transaction_id} for Reservation {self.reservation.reservation_number}"

    class Meta:
        verbose_name = "Payment"
        verbose_name_plural = "Payments"


class ManagerBooking(Booking):
    class Meta:
        proxy = True

    def can_cancel(self):
        return self.status in ["pending", "confirmed"]

class GuestBooking(Booking):
    class Meta:
        proxy = True

    def can_cancel(self):
        return self.status == "pending"