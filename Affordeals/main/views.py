from django.shortcuts import render, redirect
from django.contrib import messages 
from .forms import CustomUserCreationForm, UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.decorators import login_required
from store.models import Products, ShoppingCart, ShoppingCartItem, ShoppingOrder
from django.core.paginator import Paginator


from store.serializers import ProductsSerializer
from rest_framework.viewsets import ModelViewSet
from store.permissions import IsAdminOrReadOnly
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
def product_view(request):
    products = Products.objects.all()
    ordered_products = products.order_by('category_id')
    paginator = Paginator(ordered_products, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'main/home.html', {'page_obj': page_obj})


@login_required
def account(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST,
                                   instance=request.user)
        profile_form = ProfileUpdateForm(request.POST,
                                         request.FILES,
                                         instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, f'Your account has been successully updated!')
            return redirect('account')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)
    
    context = {
            'user_form': user_form,
            'profile_form': profile_form
        }

    return render(request, 'main/account.html', context)    