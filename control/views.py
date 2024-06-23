from django.shortcuts import render, redirect
from .forms import CustomLoginForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test

def login_view(request):
    if request.method == 'POST':
        form = CustomLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                if user.is_superuser or user.is_staff:
                    login(request, user)  # This is the correct usage
                    return redirect('control_panel')
                else:
                    form.add_error(None, 'You do not have access to the control panel.')
            else:
                form.add_error(None, 'Invalid username or password.')
    else:
        form = CustomLoginForm()
    return render(request, 'admin/login.html', {'form': form})

@login_required
@user_passes_test(lambda u: u.is_superuser or u.is_staff)
def control_panel(request):
    # Your control panel logic here
    return render(request, 'admin/control_panel.html')

def custom_logout(request):
    logout(request)
    return redirect('custom_login')
