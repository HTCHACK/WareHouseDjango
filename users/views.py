from django.db.models.fields import EmailField
from django.shortcuts import redirect, render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import logout
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm
from warehouseapp.models import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as views_auth

from .form import *



def logout_view(request):
    """Log the user out."""

    logout(request)

    return HttpResponseRedirect(reverse('store:index'))

def role(request):
    return render(request, 'users/role.html')

def register(request):
    """Register a new user."""
    if request.method != 'POST':
    # Display blank registration form.
        form = RegisterForm()
        if request.user.is_superuser :
            return redirect('/admin')
        else:
            return redirect('/profile')
    else:
        
        form = RegisterForm(data=request.POST)


        if form.is_valid():
            form.save()
            # Log the user in and then redirect to home page.
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password1')
            user = authenticate(first_name=first_name,last_name=last_name, username=username,email=email, password=password)
            login(request, user)
            return HttpResponseRedirect(reverse('users  :profile'))
    context = {'form': form}
    return render(request, 'users/register.html', context)

class LoginView(views_auth.LoginView):
    form_class=RegisterForm
    redirect_authenticated_user=True

    def get_success_url(self):
        # write your logic here
        if self.request.user.is_superuser:
            return '/admin'
        return '/'

@login_required
def profile(request):
    return render(request, 'users/profile.html')


@login_required
def receive_list(request):
    return render(request, 'users/receive_list.html')
