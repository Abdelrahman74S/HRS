from django.contrib.auth.mixins import LoginRequiredMixin , UserPassesTestMixin
from accounts.models import User
from rooms.models import Room

class IsGuest(LoginRequiredMixin , UserPassesTestMixin):
    raise_exception = True
    
    def test_func(self):
        user = self.request.user
        
        return user.is_authenticated and user.user_type == 'G'