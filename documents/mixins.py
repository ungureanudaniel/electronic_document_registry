from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import redirect

class ApprovedRequiredMixin(UserPassesTestMixin):
    """
    Mixin to ensure the user is both authenticated and approved by an admin.
    Unapproved users are redirected to a pending approval notice page.
    """
    def test_func(self):
        user = self.request.user
        return user.is_authenticated and getattr(user, 'is_approved', False)

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            return redirect('userlist')
        return redirect('login')