import re
from django.urls import reverse
from django.shortcuts import redirect
from django.http import HttpResponse


class GlobalLoginRequiredMiddleware:
    """
    Middleware that will redirect all non-authenticated users to the login page,
    except for the views in 'EXEMPT_URLS'.
    """
    EXEMPT_URLS = [
        'login', 'job_listing', 
    ]

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.user.is_authenticated:
            path = request.path_info
            exempt_urls = [reverse(url) for url in self.EXEMPT_URLS]

            
            if path in exempt_urls or path.startswith('/admin/') or ('jobs-at-linksoft' in path and path.endswith('/apply/')):
                pass  # Allow access without authentication
            else:
                return redirect('login')

        response = self.get_response(request)
        return response
