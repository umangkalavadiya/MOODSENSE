from django.shortcuts import render,redirect

from django.contrib.auth.decorators import login_required
from django.contrib.auth import login,authenticate,logout
from django.contrib.auth.models import User
from django.contrib import messages
from .utils import paginate
from .models import Profile
from .forms import CustomUserCreationForm,ProfileForm,RoleForm
from django.core.mail import send_mail
from django.conf import settings

from django.contrib.auth.models import Group
# Create your views here.

def home(request):
    return render(request,'home.html')

def loginUser(request):
    page='login'
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == "POST":
        username = request.POST['username'].lower()
        password = request.POST['password']

        try:
            user = User.objects.get(username=username)
        except:
             messages.error(request,'Username does not exit')
        
        user = authenticate(request,username=username,password=password)

        if user is not None:
            login(request,user)
            return redirect(request.GET['next'] if 'next' in request.GET else 'account')
        
        else:
            messages.error(request,'Username or password is incorrect')

    return render(request,'users/login_register.html')

def logoutUser(request):
    messages.error(request,'User was logged out')
    logout(request)
    return redirect('login')


def registerUser(request):
    page = 'register'
    form = CustomUserCreationForm()
    roleform = RoleForm()
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        roleform = RoleForm(request.POST)
        role = request.POST['role']
        if form.is_valid() and roleform.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            group = Group.objects.get(name=role)
            user.groups.add(group)
            profile = Profile.objects.create(
                user=user,
                username=user.username,
                email=user.email,
                name=user.first_name,
                role=role
            )

            subject = 'Welcome to MOODSENSE'
            message = 'We are glad you are here!'

            send_mail(
                subject,
                message,
                settings.EMAIL_HOST_USER,
                [profile.email],
                fail_silently=False,
            )
            messages.success(request,'User account was created')

            login(request,user)
            return redirect('edit-account')
        
        else:
            messages.error(request,'An error has occurred during registration')

    context={'page':page,'form':form,'roleform':roleform}
    return render(request,'users/login_register.html',context)



def userProfile(request,pk):
    profile = Profile.objects.get(id=pk)
    
    context = {'profile':profile}
    return render(request,'users/user-profile.html',context)


@login_required(login_url='login')
def userAccount(request):
    profile = request.user.profile
   
    context={'profile':profile}
    return render(request,'users/account.html',context)

@login_required(login_url='login')
def editAccount(request):
    profile = request.user.profile
    form = ProfileForm(instance=profile)

    if request.method=='POST':
        form = ProfileForm(request.POST,request.FILES,instance=profile)

        if form.is_valid():
            form.save()
            return redirect('account')

    context={'form':form}
    return render(request,'users/profile_form.html',context)

@login_required(login_url='login')
def timetable(request):
    return render(request,'timetable.html')

@login_required(login_url='login')
def recording(request):
    return render(request,'recording.html')

