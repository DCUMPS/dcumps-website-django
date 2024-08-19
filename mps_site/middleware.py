# middleware.py
from django.http import HttpResponsePermanentRedirect

class CaseInsensitiveMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Convert the path to lowercase
        lowercase_path = request.path_info.lower()
        
        if request.path_info != lowercase_path:
            return HttpResponsePermanentRedirect(lowercase_path)
        
        request.path_info = lowercase_path
        response = self.get_response(request)
        return response
