from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.contrib.auth import authenticate, login as dj_login
from .models import PropertyManager, CustomUser, Listing, Lead
from django.contrib import messages
from datetime import datetime
from django.utils.dateparse import parse_date
from django.http import JsonResponse


def dashboard(request):
    return render(request, 'base.html')


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


# def create_listing(request):
#     if request.method == 'POST':
#         title = request.POST.get('title')
#         description = request.POST.get('description')
#         price = request.POST.get('price')
#         location = request.POST.get('location')
#         image = request.FILES['image']
#         print(title,description,price,location,image,"create_listining")
#         listing = Listing.objects.create(title=title,description=description,price=price,location=location,image=image)
#         listing.save()
#         return redirect('listing')
#     else:
#         return render(request,'create_list.html')


def listing(request):
    listings = Listing.objects.all()
    return render(request, 'listing.html', {'listings': listings})


def view_list(request,list_id):
    print(list_id,"list_id")
    listing = Listing.objects.get(id=list_id)
    print(listing,"listing")
    return render(request,'view_list.html',{'listings':listing})


def delete_listing(request, list_id):
    listing = Listing.objects.get(id=list_id)
    listing.delete()
    return redirect('listing')

    return render(request, 'table.html', {'listings': listings})


def leads(request):
    if request.method == 'POST':
        date = request.POST.get('date')
        person_in_charge = request.POST.get('person_in_charge')
        status = request.POST.get('status')
        tenant_met = request.POST.get('tenant_met')

        date_object = datetime.strptime(date, '%Y-%m-%d').date()
        date_object = parse_date(date)
        Lead.objects.create(date=date_object, tenant_met=tenant_met,
                            person_in_charge=person_in_charge, status=status)

    if request.method == 'GET':
        Leads_id = request.GET.get('property_manager_id')

        Lead.objects.filter(property_manager_id=Leads_id)
        return HttpResponse

    if request.method == 'DELETE':
        lead_id = request.method.get('lead_id')
        lead = Lead.objects.get(id=lead_id)
        lead.delete()

    if request.method == 'PUT':
        request_data = request.PUT.dict()
        object_id = request_data.pop('id', None)
        new_values = request_data

        if object_id is None:
            return JsonResponse({'error': 'Object ID not provided'}, status=400)

        try:
            obj = Lead.objects.get(pk=object_id)
        except Lead.DoesNotExist:
            return JsonResponse({'error': 'Object not found'}, status=404)

        for key, value in new_values.items():
            setattr(obj, key, value)

        obj.save()
        return JsonResponse({'message': 'Object updated successfully'})
