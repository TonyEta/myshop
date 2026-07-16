from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .forms import RegistrationForm, LoginForm
import uuid


def register_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            
            base_name = user.email.split('@')[0]
            user.username = f'{base_name}_{uuid.uuid4().hex[:4]}'
            user.set_password(form.cleaned_data['password'])
            user.save()

            login(request, user, backend='django.contrib.auth.backends.ModelBackend')

            return redirect('home')
    else:
        form = RegistrationForm()

    return render(request, 'users/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')

            user = authenticate(request, username=email, password=password)
            
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                error_message = "Неправильний логін або пароль"
                return render(request, 'users/login.html', {'form': form, 'error': error_message})
    else:
        form = LoginForm()
    
    return render(request, 'users/login.html', {'form': form})

def logout_view(request):
    print("--- ФУНКЦІЯ ВИХОДУ СПРАЦЮВАЛА! ---")
    logout(request)
    return redirect('home')