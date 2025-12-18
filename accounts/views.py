from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, login, logout
from .models import Profile

# Create your views here.

def login_page(request):
    
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        user_obj = User.objects.filter(username = email)

        if not user_obj.exists():
            messages.warning(request, "Account not found")
            return HttpResponseRedirect(request.path_info)

        if not user_obj[0].profile.is_email_verified:
            messages.warning(request, "Your account has not verified")
            return HttpResponseRedirect(request.path_info)

        user_obj = authenticate(username= email, password = password)        
        
        if user_obj:
            login(request, user_obj)
            return redirect("/")

        messages.warning(request, "Invalid Credentials")
        return HttpResponseRedirect(request.path_info)

    return render(request, 'accounts/login.html')

def register_page(request):

    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')

        user_obj = User.objects.filter(username = email)

        if user_obj.exists():
            messages.warning(request, "Email is already taken")
            return HttpResponseRedirect(request.path_info)
        
        user_obj = User.objects.create(first_name = first_name, last_name = last_name, email = email, username = email)
        user_obj.set_password(password)
        user_obj.save()

        messages.success(request, "Mail has been sent")

        return HttpResponseRedirect(request.path_info)

    return render(request, "accounts/register.html")


def logout_page(request):
    logout(request)
    messages.success(request, "Logged out successfully")
    return redirect("/")


def activate_email(request, email_token):
    try:
        user = Profile.objects.get(email_token = email_token)
        user.is_email_verified = True
        user.save()
        messages.success(request, "Email verified successfully")
        return redirect("/")
    except Exception as e:
        messages.error(request, "Invalid Email Token")
        return redirect("/")


def account_page(request):
    """Account/Profile page"""
    if not request.user.is_authenticated:
        messages.warning(request, "Please login to access your account")
        return redirect('login')
    
    profile, created = Profile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        # Update user info
        user = request.user
        user.first_name = request.POST.get('first_name', user.first_name)
        user.last_name = request.POST.get('last_name', user.last_name)
        user.email = request.POST.get('email', user.email)
        user.save()
        
        # Update profile
        profile.phone_number = request.POST.get('phone_number', '')
        profile.date_of_birth = request.POST.get('date_of_birth') or None
        profile.gender = request.POST.get('gender', '')
        profile.alternate_phone = request.POST.get('alternate_phone', '')
        profile.address_line_1 = request.POST.get('address_line_1', '')
        profile.address_line_2 = request.POST.get('address_line_2', '')
        profile.city = request.POST.get('city', '')
        profile.state = request.POST.get('state', '')
        profile.postal_code = request.POST.get('postal_code', '')
        profile.country = request.POST.get('country', 'India')
        profile.save()
        
        messages.success(request, "Profile updated successfully")
        return redirect('account')
    
    context = {
        'profile': profile
    }
    return render(request, 'accounts/account.html', context)
