from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from .forms import CreateUserForm


# Create your views here.

def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request.POST)
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(username, password)
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('/blog')
        else:
            return render(request, 'account/login.html', {'form': form})
    else :
        form = AuthenticationForm()
        return render(request, 'account/login.html', {'form': form})


def register(request):
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(request, username=username, password=password)
            auth_login(request, user)
            return redirect('/blog')
    else:
        form = CreateUserForm()
    context = {
        'form': form
    }
    return render(request, 'account/register.html', context)


def logout_view(request):
    logout(request)
    return redirect('/blog')
