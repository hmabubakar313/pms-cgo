from django.contrib import messages
from django.shortcuts import render
from .forms import CustomUserCreationForm, UserChangeForm


def register(request):
    if request.method == 'POST':  # Corrected method checking to 'POST'
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created successfully')

    else:
        form = CustomUserCreationForm()

    context = {
        'form': form
    }

    return render(request, "user.html", context)
