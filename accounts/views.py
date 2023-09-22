from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from roommates.models import UserProfile
import re

# Create your views here.
def register(request):
    if request.method == 'POST':
        fullname = request.POST.get('full-name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('re-password')

        # check fullname is char and space only
        if not re.fullmatch(r'[A-Za-z ]+', fullname):
            messages.error(request, 'Invalid fullname. Only characters and spaces allowed')
            return render(request, 'accounts/signup.html')

        # check valid email
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        if not re.fullmatch(regex, email):
            messages.error(request, 'Invalid email')
            return render(request, 'accounts/signup.html')

        username = email.split('@')[0]
        if User.objects.filter(username=username).exists():
            username = username + \
                str(User.objects.filter(username=username).count())

        if password != password2:
            messages.error(request, 'Passwords do not match')
            return render(request, 'accounts/signup.html')
        if len(password) < 6:
            messages.error(request, 'Password must be at least 6 characters')
            return render(request, 'accounts/signup.html')
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists')
            return render(request, 'accounts/signup.html')

        user = User.objects.create_user(username, email, password)
        if ' ' in fullname:
            user.first_name = ' '.join(fullname.split(' ')[:-1])
            user.last_name = fullname.split(' ')[-1]
        else:
            user.first_name = fullname
        user.save()

        userProfile = UserProfile.objects.get_or_create(
            user=user,
            full_name=fullname,
        )[0]
        userProfile.save()

        # login user
        user = authenticate(request, username=username, password=password)
        login(request, user)
        return redirect('main:home')
    return render(request, 'accounts/signup.html')

def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is None:
            # try to authenticate with email
            try:
                user = User.objects.get(email=username)
                user = authenticate(
                    request, username=user.username, password=password)
            except User.DoesNotExist:
                messages.error(request, 'Invalid username or password')
                return render(request, 'accounts/login.html')

        if user is not None:
            login(request, user)
            return redirect('main:home')
        else:
            messages.error(request, 'Invalid username or password')
            return render(request, 'accounts/login.html')
        
    return render(request, 'accounts/login.html')

def logoutUser(request):
    logout(request)
    return render(request, 'accounts/login.html')