from django.shortcuts import render, redirect, get_object_or_404
from .models import Client
from .forms import ClientForm
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required, user_passes_test

def clients(request):
    client_list = Client.objects.all().order_by('name')
    paginator = Paginator(client_list, 8) 
    page_number = request.GET.get('page')
    clients = paginator.get_page(page_number)
    context = {'clients': clients}
    return render(request, 'clients.html', context)

@login_required
@user_passes_test(lambda u: u.is_superuser)
def add_client(request):
    if request.method == 'POST':
        form = ClientForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('clients')
    else:
        form = ClientForm()
    return render(request, 'add_client.html', {'form': form})

@login_required
@user_passes_test(lambda u: u.is_superuser)
def delete_client(request, client_id):
    if request.method == 'POST':
        client = get_object_or_404(Client, id=client_id)
        client.delete()
    return redirect('clients')

@login_required
@user_passes_test(lambda u: u.is_superuser)
def edit_client(request, client_id):
    client = get_object_or_404(Client, id=client_id)
    if request.method == 'POST':
        form = ClientForm(request.POST, request.FILES, instance=client)
        if form.is_valid():
            form.save()
            return redirect('clients')
    else:
        form = ClientForm(instance=client)
    return render(request, 'edit_client.html', {'form': form, 'client': client})
