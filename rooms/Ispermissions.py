from django.contrib.auth.mixins import LoginRequiredMixin , UserPassesTestMixin
from accounts.models import User
from rooms.models import Room

class IsManager(LoginRequiredMixin , UserPassesTestMixin):
    raise_exception = True
    
    def test_func(self):
        user = self.request.user
        
        return user.is_authenticated and user.user_type == 'M'

# class IsOwner(IsManager):
#     def test_func(self):
#         if not super().test_func():
#             return False
            
#         obj = self.get_object()
        
#         return self.request.user == obj.owner