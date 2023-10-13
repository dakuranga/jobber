# user_management/views.py

from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.views import View

class LoginView(View):
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            return redirect('dashboard')  # Redirect to your dashboard page
        else:
            return render(request, 'login.html', {'error': 'Invalid login credentials'})
