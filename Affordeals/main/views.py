from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm

# Create your views here.

def home(request):
    form = UserCreationForm()
    return render(request, 'main/index.html', {'form': form})

