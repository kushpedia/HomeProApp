from django.shortcuts import render, redirect
from django.http.response import HttpResponse
from .forms import CustomUserCreationForm, ProfileForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib import messages
# Create your views here.
def homepage(request):
    return render(request, "users/userhome.html")
    # return HttpResponse("Welcome")  
def userRegistration(request):
    form = CustomUserCreationForm()
    context = {'form':form}
    if request.method =="POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            messages.success(request, "User Created Succesfully")
            login(request, user)
            return redirect('edit-account')
        else:
            messages.error(request, "User Creation Failed.")
    return render(request, 'users/register.html', context)

# user Account:
@login_required(login_url='login')
def userAccount(request):
    profile = request.user.profile

    context = {'profile': profile}
    return render(request, 'users/account.html', context)
# edit account
@login_required(login_url='login')
def editAccount(request):
    profile = request.user.profile
    form = ProfileForm(instance=profile)
    # uneditable_fields = ['user']
    # for field in uneditable_fields:
    #     if field in form.fields:
    #         form.fields[field].disabled = True
            
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance = profile)
        if form.is_valid():
            form.save()
            context = {
                'user' : request.user
            }
            messages.error(request, "User Updated Successfully.")
            return redirect('homepage')

    context = {'form':form}

    return render(request, 'users/profile_form.html', context)

#Login User
def loginUser(request):
    
    if request.user.is_authenticated:
        return redirect('homepage')


    if request.method == 'POST':
        username = request.POST['username'].lower()
        password = request.POST['password']

        try:
            user = User.objects.get(username=username)
        except:
            messages.info(request, "Username Does not exist")
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect (request.GET['next'] if 'next' in request.GET else 'homepage')
        else:
            messages.error(request, "Wrong Username OR Password!")

    return render(request, 'users/login.html')

def logoutUser(request):
    logout(request)
    messages.info(request, "User Logged Out Succesfully")
    return redirect('login')