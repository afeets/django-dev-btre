from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.contrib.auth.models import User
# Create your views here.
def register(request):
    if request.method == 'POST':
        # messages.error(request, 'Testing Error')
        # return redirect('register')

        # Register User, Get form values
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        # Check if Passwords match
        if password1 == password2:
            # Check if username already exists
            if User.objects.filter(username=username).exists():
                messages.error(request, 'That username is already taken')
                return redirect('register')
            else:
                if User.objects.filter(email=email).exists():
                    messages.error(request, 'That email address is already being used')
                    return redirect('register')
                else:
                    # Looks good, create user
                    user = User.objects.create_user(username=username,password=password1,email=email,first_name=first_name,last_name=last_name)

                    # redirect after register
                    user.save()
                    messages.success(request,'You are now registered')
                    return redirect('login')
        else:
            # message error
            messages.error(request,'Passwords do not match')
            return redirect('register')
    else:
        return render(request,'accounts/register.html')

def login(request):
    if request.method == 'POST':
        # Login User
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username,password=password)

        if user is not None:
            auth.login(request, user)
            messages.success(request,'You are now logged in')
            return redirect('dashboard')
        else:
            messages.error(request,'Invalid credentials')
            return redirect('login')
    else:
        return render(request,'accounts/login.html')

def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        messages.success(request,'You are now logged out')
        return redirect('index')

def dashboard(request):
    return render(request,'accounts/dashboard.html')
