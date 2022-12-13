from django.shortcuts import render,redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth import logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from .forms import CustomAuthenticationForm,CustomUserCreationForm
# from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
User = get_user_model()
# Create your views here.


def admin_login(request):
    """Authenticate against the settings ADMIN_LOGIN and ADMIN_PASSWORD.

    Use the login email and a hash of the password."""
    form = CustomAuthenticationForm
    if request.method == 'POST':
        form = CustomAuthenticationForm(request.POST)
        email = request.POST.get('email')
        password = request.POST.get('password')
        if email and password:
            user_obj = authenticate(email=email,password=password)
            print(user_obj)
            if user_obj is not None and user_obj.is_admin:  # and user_obj.is_superuser
                login(request, user_obj)
                messages.info(request, f"You are now logged in as {email}.")
                return redirect('/')
            else:
                messages.error(request,'Incorrect Username or Password')
    context = {'form': form}
    return render(request, 'account/login.html', context)

def logout_view(request):
    logout(request)
    messages.success(request,"Logged Out Sucessfully!")
    return redirect('/account/login')

def signupView(request):
    """ User sign up form """
    form = CustomUserCreationForm
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Congratulations !! Registered sucessfully')
            return redirect('/')
        else:
            messages.error(request, 'Something went wrong! please try again!')
            return redirect('/account/signup')
    context = {'form': form}
    return render(request, 'account/sign_up.html', context)



