from django.shortcuts import render

def emailclient(request):
    return render(request, 'emailclient.html')
