from django.db import models
from .Utils import generate_unique_room_number 
from django.utils.text import slugify

class Amenity(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name

class RoomType(models.Model):
    BED_CHOICES = [('S', 'Single'), ('D', 'Double'), ('K', 'King')]
    
    name = models.CharField(max_length=50)
    slug = models.SlugField(unique=True, blank=True, null=True) 
    description = models.TextField(blank=True, null=True)
    base_price = models.DecimalField(max_digits=10, decimal_places=2)
    max_occupancy = models.PositiveIntegerField()
    bed_type = models.CharField(choices=BED_CHOICES, max_length=1, default='S')
    size_sqm = models.PositiveIntegerField()
    image = models.ImageField(upload_to='room_types/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    amenities = models.ManyToManyField(Amenity, blank=True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Room(models.Model):
    STATUS_CHOICES = [('A', 'Available'), ('O', 'Occupied'), ('M', 'Maintenance'), ('C', 'Cleaning')]
    room_number = models.CharField(max_length=10, unique=True, editable=False) 
    room_type = models.ForeignKey(RoomType, on_delete=models.CASCADE, related_name='rooms')
    floor = models.IntegerField()
    status = models.CharField(choices=STATUS_CHOICES, max_length=1, default='A')
    is_active = models.BooleanField(default=True)
    notes = models.TextField(blank=True, null=True)
    slug = models.SlugField(unique=True, blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    pricing_override = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.room_number:
            self.room_number = generate_unique_room_number(self)
        
        if not self.slug:
            self.slug = slugify(f"room-{self.room_number}") 
            
        super(Room, self).save(*args, **kwargs)

    def __str__(self):
        return f"Room {self.room_number} ({self.room_type.name})"
    
class RoomImage(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='hotel_images/')
    is_primary = models.BooleanField(default=False) 
    caption = models.CharField(max_length=100, blank=True) 
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    def save(self, *args, **kwargs):
        if self.is_primary:
            RoomImage.objects.filter(room=self.room, is_primary=True).update(is_primary=False)
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['-is_primary', 'uploaded_at']
        
    def __str__(self):
        return f"Image for Room {self.room.room_number}"