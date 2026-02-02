from django.contrib.auth.mixins import LoginRequiredMixin , UserPassesTestMixin
from accounts.models import User


class IsManager(LoginRequiredMixin , UserPassesTestMixin):
    raise_exception = True
    
    def test_func(self):
        user = self.request.user
        user.is_authenticated and user.user_type == 'M'
