from .forms import SignupForm, ChangePasswordForm, EditProfileForm
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from .models import Profile
from classroom.models import Course
# Create your views here.

def UserProfile(request, username):
    user = get_object_or_404(User, username=username)
    courses_count = Course.objects.filter(user=user).count()
    profile = Profile.objects.get(user=user)


    context = {
        'profile': profile,
        'courses_count': courses_count,

    }

    return render(request,'registration/profile.html',context)

def Signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            User.objects.create_user(
                username=username, email=email, password=password)
            return redirect('edit-profile')
    else:
        form = SignupForm()

    context = {
        'form': form,
    }

    return render(request, 'registration/signup.html', context)


@login_required
def PasswordChange(request):
    user = request.user
    if request.method == 'POST':
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            new_password = form.cleaned_data.get('new_password')
            user.set_password(new_password)
            user.save()
            update_session_auth_hash(request, user)
            return redirect('change-password-done')
    else:
        form = ChangePasswordForm(instance=user)

    context = {
        'form': form,
    }

    return render(request, 'registration/change_password.html', context)


def PasswordChangeDone(request):
    return render(request, 'registration/change_password_done.html')


@login_required
def EditProfile(request):
    profile = Profile.objects.filter(user=request.user).first()

    if request.method == 'POST':
        form = EditProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            profile.picture = form.cleaned_data.get('picture')
            profile.full_name = form.cleaned_data.get('full_name')
            profile.banner = form.cleaned_data.get('banner')
            profile.location = form.cleaned_data.get('location')
            profile.url = form.cleaned_data.get('url')
            profile.profile_info = form.cleaned_data.get('profile_info')
            profile.save()
            return redirect('user-profile',username=request.user.username)
    else:
        form = EditProfileForm(instance=profile)

    context = {
        'form': form,
    }

    return render(request, 'registration/edit_profile.html', context)
