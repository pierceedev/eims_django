from django.contrib.auth.mixins import AccessMixin
from django.http import HttpResponse
from django.shortcuts import redirect


class UserTypeRequiredMixin(AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        user_type = self.get_user_type()
        if not request.user.is_authenticated or not getattr(request.user, f'is_{user_type}', False):
            return HttpResponse('Unauthorized', status=401)
        return super(UserTypeRequiredMixin, self).dispatch(request, *args, **kwargs)

    def get_user_type(self):
        raise NotImplementedError("Subclasses of UserTypeRequiredMixin must provide a get_user_type() method.")
        
class AdminRequiredMixin(UserTypeRequiredMixin):                                                                                        
    def get_user_type(self):
        return 'admin'
    
class SuperUserRequiredMixin(UserTypeRequiredMixin):
    def get_user_type(self):
        return 'superuser'
    
    def redirect_user(self, request, user_type):
        return redirect("admin:index")

    def redirect_user(self, request, user_type):
        return redirect("staffs:staff-list")
    
class SecretaryRequiredMixin(UserTypeRequiredMixin):
    def get_user_type(self):
        return 'secretary'

    def redirect_user(self, request, user_type):
        return redirect("secretary:item-list")

class DeanRequiredMixin(UserTypeRequiredMixin):
    def get_user_type(self):
        return 'dean'

    def redirect_user(self, request, user_type):
        return redirect("rlab:eq-list")

class StaffRequiredMixin(UserTypeRequiredMixin):
    def get_user_type(self):
        return 'staff'

    def redirect_user(self, request, user_type):
        return redirect("staffs:eq-borrowed-list")