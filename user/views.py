from django.shortcuts import render,redirect
from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.contrib.auth import authenticate,login as dj_login
from .models import PropertyManager,CustomUser,Listing
from django.contrib import messages


# Create your views here.

def dashboard(request):
    return render(request,'base.html')

def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        # Authenticate user using email and password
        user = authenticate(request, email=email, password=password)
        
        if user is not None:
            # Authentication successful, login the user
            dj_login(request, user)
            return redirect('dashboard')  # Redirect to dashboard for PropertyManager
        elif user is not None:
            # Authentication successful, login the user
            dj_login(request, user)
            return redirect('user_dashboard')  # Redirect to user dashboard for CustomUser
        else:
            # Authentication failed, show error message
            error_message = "Invalid email or password."
            return render(request, 'login.html', {'error_message': error_message})
    else:
        # Render the login page
        return render(request, 'login.html')





def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        retype_password = request.POST.get('retype_password')
        terms_agreed = request.POST.get('terms')
        print(username,email,password,retype_password,terms_agreed,"signup")

        # Check if passwords match
        if password != retype_password:
            error_message = "Passwords do not match."
            messages.error(request, error_message)
            return render(request, 'signup.html', {'error_message': error_message})

        try:
            # Create a new user
            user = CustomUser.objects.create_user(email=email, password=password)      
            print(user,"user")
            user.save()
            property_manager = PropertyManager.objects.create(user=user, username=username)
            property_manager.save()
            messages.success(request, 'Account created successfully.')

            return redirect('login')
        except Exception as e:
            # If there's an error creating the user, handle it and show proper message
            messages.error(request, str(e))
            return render(request, 'signup.html', {'error_message': str(e)})
    else:
        # If not a POST request, render the signup page
        return render(request, 'signup.html')


def table(request):
    listings = Listing.objects.all()
    return render(request,'table.html',{'listings':listings})