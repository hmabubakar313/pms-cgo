from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.contrib.auth import authenticate,login as dj_login
from .models import PropertyManager,CustomUser,Listing,Image, Lead
from django.contrib import messages
from datetime import datetime
from django.utils.dateparse import parse_date
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

@login_required(login_url='login')
def dashboard(request):
    user = PropertyManager.objects.get(user=request.user)
    return render(request, 'base.html', {'user': user})


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
        print(username, email, password, retype_password, terms_agreed, "signup")

        # Check if passwords match
        if password != retype_password:
            error_message = "Passwords do not match."
            messages.error(request, error_message)
            return render(request, 'signup.html', {'error_message': error_message})

        try:
            # Create a new user
            user = CustomUser.objects.create_user(email=email, password=password)      
            print(user, "user")
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

@login_required(login_url='login')
def create_listing(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        price = request.POST.get('price')
        num_bedrooms = request.POST.get('num_bedrooms')
        num_bathrooms = request.POST.get('num_bathrooms')
        square_footage = request.POST.get('square_footage')
        address = request.POST.get('address')
        
        
        property_manager = PropertyManager.objects.get(user=request.user)
        
        
        
        image_file = request.FILES.get('image')
        # print("image",image)
        image_instance = Image.objects.create(image=image_file)

        
       

        # Create the Listing object
        listing = Listing.objects.create(
            property_manager=property_manager,
            title=title,
            price=price,
            num_bedrooms=num_bedrooms,
            num_bathrooms=num_bathrooms,
            square_footage=square_footage,
            address=address,
           
        )
        listing.image.add(image_instance)
        listing.save()

        return redirect('listing')  # Redirect to wherever you want

    else:
        # If not a POST request, render the form
        
        return render(request, 'create_list.html')


@login_required(login_url='login')
def listing(request):
    listings = Listing.objects.all()
    return render(request, 'listing.html', {'listings': listings})

@login_required(login_url='login')
def view_list(request,list_id):
    print(list_id,"list_id")
    listing = Listing.objects.get(id=list_id)
    print(listing,"listing")
    return render(request,'view_list.html',{'listings':listing})

@login_required(login_url='login')
def delete_listing(request, list_id):
    listing = Listing.objects.get(id=list_id)
    listing.delete()
    return redirect('listing')

    return render(request, 'table.html', {'listings': listings})

def update_listing(request, list_id):
    # Get the existing listing object from the database
    listing = get_object_or_404(Listing, id=list_id)
    
    if request.method == 'POST':
        title = request.POST.get('title')
        price = request.POST.get('price')
        num_bedrooms = request.POST.get('num_bedrooms')
        num_bathrooms = request.POST.get('num_bathrooms')
        square_footage = request.POST.get('square_footage')
        address = request.POST.get('address')
        image = request.FILES.get('image')
        
        # Update the attributes of the existing listing object
        listing.title = title
        listing.price = price
        listing.num_bedrooms = num_bedrooms
        listing.num_bathrooms = num_bathrooms
        listing.square_footage = square_footage
        listing.address = address
        
        if 'image' in request.FILES:
            image = request.FILES['image']
            listing.image = image
        
        # Save the changes to the existing listing object
        listing.save()
        
        # Redirect to a relevant page (e.g., listing detail page)
        return redirect('listing')

    # If the request method is not POST, render the update form with the existing listing object
    return render(request, 'update_list.html', {'listing': listing})


def create_lead(request):
    if request.method == 'POST':
        date = request.POST.get('date')
        person_in_charge = request.POST.get('person_in_charge')
        status = request.POST.get('status')

        lead = Lead.objects.create(date=date, person_in_charge=person_in_charge, status=status, tenant_met_id=tenant_met_id)
        return redirect('list_leads')  # Redirect to wherever you want
    else:
        return render(request, 'create_lead.html')


def list_leads(request):
    leads = Lead.objects.all()
    return render(request, 'leeds.html', {'leads': leads})

# # Update
def update_lead(request, lead_id):
    lead = get_object_or_404(Lead, id=lead_id)
    if request.method == 'POST':
        lead.date = request.POST.get('date')
        lead.person_in_charge = request.POST.get('person_in_charge')
        lead.status = request.POST.get('status')
        
        lead.save()
        return redirect('list_leads')
    else:
        return render(request, 'update_lead.html', {'lead': lead})


def delete_lead(request, lead_id):
    lead = get_object_or_404(Lead, id=lead_id)
    lead.delete()
    return redirect('list_leads')