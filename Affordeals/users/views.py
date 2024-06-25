from django.shortcuts import redirect, render
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.http import HttpResponse

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return HttpResponse('<h1> account created for user</h1>')
    else:
        form = UserCreationForm()
    return render(request, 'users/register.html', {'form': form})
