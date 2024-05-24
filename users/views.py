from django.shortcuts import render,redirect,get_object_or_404
from .forms import RegisterForm,LoginForm
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from .models import *
from userssection.models import *


def main_page(request):
    return render(request, 'index.html')



def register_page(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user =form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            form.save()
            print('wfdomnmoi')
            messages.success(request,'Registered Successfully..!')
            return redirect('mainpage')
    else:
        form = RegisterForm()
    return render(request,'register.html')

def login_page(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request,email=email,password=password)
            if user is not None:
                login(request,user)
                messages.success(request,'LoggedIn SuccessFully')
                return redirect('mainpage')
            else:
                messages.error(request, "Invalid email or password.")
        else:
            form = LoginForm()
    return render(request,'login.html')
    
def logout_page(request):
    logout(request)
    messages.success(request,'LoggedOut SuccessFully..!')
    return redirect('mainpage')

# def explore_page(request):
#     user_profiles = User.objects.all()
#     return render(request,'explore.html',{'user_profiles':user_profiles})

def explore_page(request):
    query = request.GET.get('q')
    if query:
        # Filter user profiles based on the search query
        user_profiles = User.objects.filter(username__icontains=query)
    else:
        # If no search query provided, return all user profiles
        user_profiles = User.objects.all()
    
    context = {
        'user_profiles': user_profiles,
    }
    return render(request, 'explore.html', context)