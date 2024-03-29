from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.contrib.auth import authenticate, login as dj_login
from .models import PropertyManager, CustomUser, Listing, Image, Lead, Tenant, Broker
from django.contrib import messages
from datetime import datetime
from django.utils.dateparse import parse_date
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .forms import TenantsForm, CustomUserCreationForm, UserForm, BrokerForm
from django.forms import inlineformset_factory


def home(request):
    return render(request, "login.html")


@login_required(login_url="login")
def dashboard(request):
    return render(request, "base.html")


def login(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        # Authenticate user using email and password
        user = authenticate(request, email=email, password=password)

        if user is not None:
            # Authentication successful, login the user
            dj_login(request, user)
            return redirect("dashboard")  # Redirect to dashboard for PropertyManager
        elif user is not None:
            # Authentication successful, login the user
            dj_login(request, user)
            return redirect(
                "user_dashboard"
            )  # Redirect to user dashboard for CustomUser
        else:
            # Authentication failed, show error message
            error_message = "Invalid email or password."
            return render(request, "login.html", {"error_message": error_message})
    else:
        # Render the login page
        return render(request, "login.html")


def signup(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        retype_password = request.POST.get("retype_password")
        terms_agreed = request.POST.get("terms")

        # Check if passwords match
        if password != retype_password:
            error_message = "Passwords do not match."
            messages.error(request, error_message)
            return render(request, "signup.html", {"error_message": error_message})

        try:
            # Create a new user
            user = CustomUser.objects.create_user(email=email, password=password)
            user.save()
            property_manager = PropertyManager.objects.create(
                user=user, username=username
            )
            property_manager.save()
            messages.success(request, "Account created successfully.")

            return redirect("login")
        except Exception as e:
            # If there's an error creating the user, handle it and show proper message
            messages.error(request, str(e))
            return render(request, "signup.html", {"error_message": str(e)})
    else:
        # If not a POST request, render the signup page
        return render(request, "signup.html")


@login_required(login_url="login")
# @login_required(login_url='login')
def create_listing(request):
    if request.method == "POST":
        title = request.POST.get("title")
        price = request.POST.get("price")
        num_bedrooms = request.POST.get("num_bedrooms")
        num_bathrooms = request.POST.get("num_bathrooms")
        square_footage = request.POST.get("square_footage")
        address = request.POST.get("address")

        property_manager = PropertyManager.objects.get(user=request.user)

        image_file = request.FILES.get("image")
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

        return redirect("listing")  # Redirect to wherever you want

    else:
        # If not a POST request, render the form

        return render(request, "create_list.html")


@login_required(login_url="login")
def listing(request):
    listings = Listing.objects.all()
    return render(request, "listing.html", {"listings": listings})


@login_required(login_url="login")
def view_list(request, list_id):
    listing = Listing.objects.get(id=list_id)
    return render(request, "view_list.html", {"listings": listing})


@login_required(login_url="login")
def delete_listing(request, list_id):
    listing = Listing.objects.get(id=list_id)
    listing.delete()
    return redirect("listing")

    return render(request, "table.html", {"listings": listings})


@login_required(login_url="login")
def update_listing(request, list_id):
    # Get the existing listing object from the database
    listing = get_object_or_404(Listing, id=list_id)

    if request.method == "POST":
        title = request.POST.get("title")
        price = request.POST.get("price")
        num_bedrooms = request.POST.get("num_bedrooms")
        num_bathrooms = request.POST.get("num_bathrooms")
        square_footage = request.POST.get("square_footage")
        address = request.POST.get("address")
        image = request.FILES.get("image")

        # Update the attributes of the existing listing object
        listing.title = title
        listing.price = price
        listing.num_bedrooms = num_bedrooms
        listing.num_bathrooms = num_bathrooms
        listing.square_footage = square_footage
        listing.address = address

        if "image" in request.FILES:
            image = request.FILES["image"]
            listing.image = image

        # Save the changes to the existing listing object
        listing.save()

        # Redirect to a relevant page (e.g., listing detail page)
        return redirect("listing")

    # If the request method is not POST, render the update form with the existing listing object
    return render(request, "update_list.html", {"listing": listing})


@login_required(login_url="login")
def create_lead(request):
    if request.method == "POST":
        date_time = request.POST.get("datetime")
        print("date_time:", date_time)
        datetime_object = datetime.strptime(date_time, "%Y-%m-%dT%H:%M")
        person_in_charge = request.POST.get("person_in_charge")
        status = request.POST.get("status")
        tenant_met_id = request.POST.get("tenant")
        notes = request.POST.get("notes")
        Lead.objects.create(
            datetime=datetime_object,
            person_in_charge=person_in_charge,
            status=status,
            tenant_met_id=tenant_met_id,
            notes=notes,
        )

        return redirect("list_leads")
    tenants = Tenant.objects.all()
    context = {
        'tenants': tenants
    }
    return render(request, "create_lead.html", context)


@login_required(login_url="login")
def list_leads(request):
    leads = Lead.objects.all()
    tenants = Tenant.objects.all()

    return render(request, "leeds.html", {"leads": leads, "tenants": tenants})


# # Update
@login_required(login_url="login")
def update_lead(request, lead_id):
    lead = get_object_or_404(Lead, id=lead_id)
    if request.method == "POST":
        date_time = request.POST.get("datetime")
        datetime_object = datetime.strptime(date_time, "%Y-%m-%dT%H:%M")
        lead.datetime = datetime_object
        lead.person_in_charge = request.POST.get("person_in_charge")
        lead.status = request.POST.get("status")

        lead.save()
        return redirect("list_leads")
    else:
        return render(request, "update_lead.html", {"lead": lead})


@login_required(login_url="login")
def delete_lead(request, lead_id):
    lead = get_object_or_404(Lead, id=lead_id)
    lead = Lead.objects.delete(id=lead_id)
    lead.delete()
    return redirect("list_leads")


@login_required(login_url="login")
def view_lead(request, lead_id):
    lead = Lead.objects.get(id=lead_id)
    return render(request, "view_leed.html", {"lead": lead})


@login_required(login_url="login")
def list_tenants(request):
    tenants = Tenant.objects.all()
    return render(request, "tenant.html", {"tenants": tenants})


@login_required(login_url="login")
def create_tenant(request):
    # Ensure property manager is associated with the current user
    property_manager = PropertyManager.objects.get(user=request.user)
    if request.method == "POST":
        # Populate both tenant and user form data from the request
        tenant_form = TenantsForm(request.POST)
        user_form = UserForm(request.POST)
        # Check if both forms are valid
        if tenant_form.is_valid() and user_form.is_valid():
            # Save the user first
            user = user_form.save()
            # Save the tenant associated with the property manager and user
            tenant = tenant_form.save(commit=False)
            tenant.property_manager = property_manager
            tenant.user = user
            tenant.save()
            # Redirect to the list of tenants
            return redirect("list_tenants")
        else:
            print("User form errors:", user_form.errors)
    else:
        tenant_form = TenantsForm()
        user_form = CustomUserCreationForm()
    return render(
        request,
        "create_tenant.html",
        {"tenant_form": tenant_form, "user_form": user_form},
    )


@login_required(login_url="login")
def delete_tenant(request, tenant_id):
    tenant = Tenant.objects.get(id=tenant_id)
    tenant.delete()
    return redirect("list_tenants")


@login_required(login_url="login")
def update_tenant(request, tenant_id):
    tenant = Tenant.objects.get(id=tenant_id)
    if request.method == "POST":
        tenant.name = request.POST.get("name")
        tenant.email = request.POST.get("email")
        tenant.password = request.POST.get("password")
        tenant.save()
        return redirect("list_tenants")
    else:
        return render(request, "update_tenant.html", {"tenant": tenant})

@login_required(login_url="login")
def view_tenant(request, tenant_id):
    tenant = Tenant.objects.get(id=tenant_id)
    return render(request, "view_tenant.html", {"tenant": tenant})

@login_required(login_url="login")
def create_broker(request):
    # Ensure property manager is associated with the current user
    property_manager = PropertyManager.objects.get(user=request.user)

    if request.method == "POST":
        print("Request POST data:", request.POST)
        # Populate both broker and user form data from the request
        broker_form = BrokerForm(request.POST)
        user_form = UserForm(request.POST)

        # Check if both forms are valid
        if broker_form.is_valid() and user_form.is_valid():
            print("Broker form data:")
            # Save the user first
            user = user_form.save()
            # Save the broker associated with the property manager and user
            broker = broker_form.save(commit=False)
            broker.property_manager = property_manager
            broker.user = user
            broker.save()
            # Redirect to the list of brokers
            return redirect("broker_list")
        else:
            print("User form errors:", user_form.errors)
    else:
        print("in the else")
        broker_form = BrokerForm()
        user_form = CustomUserCreationForm()

    return render(
        request,
        "create_broker.html",
        {"broker_form": broker_form, "user_form": user_form},
    )

@login_required(login_url="login")
def delete_broker(request, broker_id):
    broker = get_object_or_404(Broker, id=broker_id)
    broker.delete()
    return redirect("broker_list")

@login_required(login_url="login")
def update_broker(request, broker_id):
    broker = Broker.objects.get(id=broker_id)
    if request.method == "POST" and broker_id:
        form = TenantsForm(request.POST, instance=broker)
        broker.name = request.POST.get("name")
        broker.email = request.POST.get("email")
        broker.password = request.POST.get("password")
        broker.password = request.POST.get("commission_rate")
        broker.save()
        return redirect("broker_list")
        # if form.is_valid():
        #     form.save()
    return render(request, "update_broker.html", {"broker": broker})

@login_required(login_url="login")
def broker_list(request):
    brokers = Broker.objects.all()
    return render(request, "broker.html", {"brokers": brokers})


@login_required(login_url="login")
def view_broker(request, broker_id):
    broker = Broker.objects.get(id=broker_id)
    return render(request, "view_broker.html", {"broker": broker})
