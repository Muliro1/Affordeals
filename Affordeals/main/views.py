from django.shortcuts import render, redirect
from django.contrib import messages 
from .forms import CustomUserCreationForm
from django.contrib.auth.decorators import login_required
from store.models import Products, ShoppingCart, ShoppingCartItem, ShoppingOrder
from django.core.paginator import Paginator

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
@login_required 
def account(request):
    return render(request, 'main/account.html')

@login_required
def product_view(request):
    products = Products.objects.all()
    paginator = Paginator(products, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'main/home.html', {'page_obj': page_obj})

