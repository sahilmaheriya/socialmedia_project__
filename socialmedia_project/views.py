from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

@login_required(login_url='/login/')
def home_view(request):
    return render(request, 'home.html')

def signup_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        if password1 == password2:
            User.objects.create(username = username, email = email, password = password1)
            return redirect('/login')
    else:
        return render(request, 'signup.html')
    return render(request, 'signup.html')

def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            return redirect('/login')
    else:
        return render(request, 'login.html')
    return render(request, 'login.html')

def logout_user(request):
    logout(request)
    return redirect('/login')