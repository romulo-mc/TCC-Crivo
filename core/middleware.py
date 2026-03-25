from django.shortcuts import redirect

class BloquearAdminMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith('/porta-dos-fundos/'):
            if not request.user.is_authenticated or not request.user.is_staff:
                return redirect('home')
        
        response = self.get_response(request)
        return response