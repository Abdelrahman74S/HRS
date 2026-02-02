from django.db import models
from django.contrib.auth.models import AbstractUser , BaseUserManager
import uuid
# Create your models here.

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_staff(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('user_type', 'M') 

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Staff must have is_staff=True.')

        return self.create_user(email, password, **extra_fields)
    
    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)

class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    User_picture = models.ImageField(upload_to='User_pictures/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    CHOICES = [
        ('G', 'Guest'),
        ('M', 'Manager'),
    ]

    objects = CustomUserManager()
    user_type = models.CharField(max_length=1, choices=CHOICES, default='G')
    loyalty_points = models.IntegerField(default=0)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    def save(self, *args, **kwargs):
        if self.is_superuser:
            self.user_type = 'M'
            self.is_staff = True
        else:
            if self.user_type == 'M':
                self.is_staff = True
            else:
                self.is_staff = False
                
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.username} - ({self.email})"
    
    