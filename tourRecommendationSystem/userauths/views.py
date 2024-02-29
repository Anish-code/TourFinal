from django.shortcuts import render, redirect
from userauths.forms import UserRegisterForm

from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.conf import settings
from django.contrib.auth import logout
from userauths.models import User
# Create your views here.
def register_view(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user.set_email(email)
            user.set_password(password)
            user.save()
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect("core:index")
    else:
        form = UserRegisterForm()

        context = {'form': form}
        return render(request, 'userauths/sign-in.html', context)

# def register_view(request):
#     if request.method == "POST":
#         form = UserRegisterForm(request.POST)
#         if form.is_valid():
#             new_user = form.save()
#             username = form.cleaned_data.get("username")
#             messages.success(request, f"Hey {username}, Your account was created successfully")
#             # Ensure that authentication works with your User model setup
#             new_user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
#             if new_user:
#                 login(request, new_user)
#                 # Ensure the correct redirect URL after login
#                 return redirect("core:index")
#             else:
#                 messages.error(request, "Failed to authenticate user after registration.")
#     else:
#         form = UserRegisterForm()

#     context = {'form': form}
#     return render(request, "userauths/sign-in.html", context)


def login_view(request):
    if request.user.is_authenticated:
        messages.warning(request, f"Hey you are already logged in.")
        return redirect ("core:index")
    
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        
        try:
            user = User.objects.get(email=email)
            
            # user = authenticate(request, email=email, password= password)
            user = authenticate(request, email=email, password=password)

        
            if user is not None:
                login(request, user)
                messages.success(request, "you are logged in")
                return redirect("core:index")
            else:
                messages.warning(request, "User doesn't exist , create an account")
            
        except:
            messages.warning(request, f"User with {email} doesnot exist")
            
                 
    context = {
        
    }
    return render(request, "userauths/sign-in.html", context)


def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out")
    return redirect("userauths:sign-in")
            
        