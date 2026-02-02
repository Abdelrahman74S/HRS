from django.contrib import admin
from .models import Amenity, RoomType, Room, RoomImage

class RoomImageInline(admin.TabularInline):
    model = RoomImage
    extra = 2  
    fields = ['image', 'is_primary', 'caption']

@admin.register(Amenity)
class AmenityAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']

@admin.register(RoomType)
class RoomTypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'base_price', 'bed_type', 'max_occupancy', 'is_active']
    list_filter = ['bed_type', 'is_active']
    search_fields = ['name']
    prepopulated_fields = {"slug": ("name",)} 

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ['room_number', 'room_type', 'floor', 'status', 'is_active']
    
    list_filter = ['status', 'room_type', 'floor', 'is_active']
    
    search_fields = ['room_number']
    
    readonly_fields = ['room_number', 'slug', 'created_at', 'updated_at']
    
    inlines = [RoomImageInline]
    
    fieldsets = (
        ('Basic Info', {
            'fields': ('room_number', 'slug', 'room_type', 'floor')
        }),
        ('Status & Availability', {
            'fields': ('status', 'is_active')
        }),
        ('Additional Notes', {
            'fields': ('notes',),
            'classes': ('collapse',) 
        }),
    )
    

admin.site.site_header = "Hotel Management System"
admin.site.site_title = "Control Panel"
admin.site.index_title = "Welcome to the hotel management"