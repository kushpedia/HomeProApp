from django.shortcuts import render, redirect
from django.http.response import HttpResponse
from .forms import CustomUserCreationForm, ProfileForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Profile
from django.core.mail import EmailMessage, send_mail
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from . tokens import generate_token
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_str
from homepro import settings
from django.contrib.auth.tokens import default_token_generator
from django.urls import reverse
from django.contrib.auth import get_user_model
User = get_user_model()
# Create your views here.
def homepage(request):
    return render(request, "users/userhome.html")

#user registration
def userRegistration(request):
    form = CustomUserCreationForm()    
    if request.method =="POST":
        form = CustomUserCreationForm(request.POST)
        email = request.POST.get("email")
        if User.objects.filter(email=email).exists():
            messages.error(request, "A user with this email already exists. Please use a different email.")
            return redirect('register')
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            messages.success(request, "User Created Succesfully, an activation link has been sent to you email")
            
            # Welcome Email
            subject = "Welcome to Homepro by Kushpedia"
            message = "Hello " + user.first_name + "!! \n" + "Welcome to Homepro!! \nThank you for visiting our website\n. We have also sent you a confirmation email, please confirm your email address. \n\nThanking You\nHenry Kuria \nCEO @Kushpedia"        
            from_email = settings.EMAIL_HOST_USER
            to_list = [user.email]
            send_mail(subject, message, from_email, to_list, fail_silently=True)            
            
            
            # send verification email
            to_list = [user.email]
            from_email = settings.EMAIL_HOST_USER
            current_site = get_current_site(request)
            email_subject = "Confirm your Email @ HomePro"
            message2 = render_to_string('users/email_confirmation.html',{
                
                'name': user.first_name,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': generate_token.make_token(user)
            })
            email = EmailMessage(
            email_subject,
            message2,
            settings.EMAIL_HOST_USER,
            [user.email],
            )
            send_mail(email_subject, message2, from_email, to_list, fail_silently=True)
            login(request, user)
            return redirect('edit-account')
        else:
            messages.error(request, "User Creation Failed. Please correct the errors below.")
    context = {'form':form}       
    return render(request, 'users/register.html', context)

#activate user through email link
def activate(request,uidb64,token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        myuser = User.objects.get(pk=uid)
    except (TypeError,ValueError,OverflowError,User.DoesNotExist):
        myuser = None

    if myuser is not None and generate_token.check_token(myuser,token):
        myuser.is_active = True
        # user.profile.signup_confirmation = True
        myuser.save()
        login(request,myuser)
        messages.success(request, "Your Account has been activated!!")
        return redirect('edit-account')
    else:
        return render(request,'users/activation_failed.html')

# user Account:
@login_required(login_url='login')
def userAccount(request):
    profile = request.user.profile
    context = {'profile': profile}
    return render(request, 'users/account.html', context)
# edit account on user creation
@login_required(login_url='login')
def editAccount(request):    
    profile, created = Profile.objects.get_or_create(user=request.user)
    form = ProfileForm(instance=profile)
    select_fields = ['role','preferred_payment_method']
    
            
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance = profile)
        if form.is_valid():
            form.save()
            messages.error(request, "User Updated Successfully.")
            return redirect('homepage')

    context = {
        'form':form,
        'select_fields' : select_fields
        }

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
        except User.DoesNotExist:
            messages.error(request, "Username does not exist")
            return redirect('login')

        # Check if the user is active before authenticating
        if not user.is_active:
            messages.warning(request, "Kindly check your email for activation, or request a new activation link.")
            return redirect('login')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.error(request, "logged In Successfully.")
            return redirect(request.GET.get('next', 'profile'))
        else:
            messages.error(request, "Wrong Username OR Password!")

    return render(request, 'users/login.html')

#forgotten password
def forgot_password(request):
    if request.method == "POST":
        email = request.POST.get('email')
        username = request.POST.get('username')

        try:
            user = User.objects.get(email=email, username=username)
        except User.DoesNotExist:
            messages.error(request, "User with this email and username does not exist.")
            return redirect('forgot_password')

        # Generate reset token
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        reset_link = request.build_absolute_uri(reverse('reset_password', kwargs={'uidb64': uid, 'token': token}))

        # Send email
        send_mail(
            "Password Reset Request",
            f"Click the link below to reset your password:\n{reset_link}",
            "noreply@yourdomain.com",
            [user.email],
            fail_silently=False,
        )

        messages.success(request, "A password reset link has been sent to your email.")
        return redirect('login')

    return render(request, 'users/forgot_password.html')

#reset password

def reset_password(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (User.DoesNotExist, ValueError):
        messages.error(request, "Invalid reset link.")
        return redirect('login')

    if not default_token_generator.check_token(user, token):
        messages.error(request, "The password reset link is invalid or expired.")
        return redirect('forgot_password')

    if request.method == "POST":
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        if new_password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect(request.path)

        user.set_password(new_password)
        user.save()
        messages.success(request, "Your password has been successfully reset. You can now log in.")
        return redirect('login')

    return render(request, 'users/reset_password.html', {'uidb64': uidb64, 'token': token})


def logoutUser(request):
    logout(request)
    messages.info(request, "User Logged Out Succesfully")
    return redirect('login')
# get user profile page
@login_required(login_url='login')
def profile(request):
    profile = request.user.profile
    context = {
        'profile': profile
    }
    return render(request, 'users/profile-page.html',context)
