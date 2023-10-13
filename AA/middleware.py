from django.urls import reverse
from django.shortcuts import redirect

class GlobalLoginRequiredMiddleware:
    """
    Middleware that will redirect all non-authenticated users to the login page,
    except for the views in 'EXEMPT_URLS'.
    """
    EXEMPT_URLS = [
        'login', 
    ]

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.user.is_authenticated:
            path = request.path_info
            exempt_urls = [reverse(url) for url in self.EXEMPT_URLS]

            if path not in exempt_urls and not path.startswith('/admin/'):
                return redirect('login')

        response = self.get_response(request)
        return response
