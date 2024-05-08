from django.shortcuts import redirect
from django.urls import reverse

class LogoutMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        
        # Check if user is logged out and not requesting the login page
        if not request.user.is_authenticated and request.path != reverse('login'):
            print("User is logged out, redirecting to login page")
            return redirect('login')

        return response
