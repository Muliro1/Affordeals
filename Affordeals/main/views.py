from django.shortcuts import render, redirect
from django.contrib import messages 
from .forms import CustomUserCreationForm

# Create your views here.

def home(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!, you are now able to login')
            return redirect('login')
    else:
        form = CustomUserCreationForm(request.POST)
    return render(request, 'main/index.html', {'form': form})

def about(request):
    return render(request, 'main/about.html')

def account(request):
    return render(request, 'main/account.html')

def product_view(request):
    return render(request, 'main/home.html')

