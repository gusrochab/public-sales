from django.contrib import messages
from django.shortcuts import render, redirect, reverse, HttpResponse
from .forms import UserRegisterForm, UserLoginForm, UserUpdateForm, UserProfileUpdateForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


def register_view(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(user.password)
            user.save()
            messages.success(
                request, f'Your Account has been created. Now you can log in')
            return redirect(reverse('login'))
        else:
            messages.error(request, form.errors)
            return redirect(reverse('register'))
    else:
        form = UserRegisterForm()
        context = {'form': form, 'title': "registration"}
        return render(request, 'users/register.html', context)


def login_view(request):
    if request.method == "POST":
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect(reverse('home'))
            else:
                return HttpResponse(form.errors)
        else:
            return HttpResponse(f'form not valid {form.errors}')

    else:
        form = UserLoginForm()
        context = {'form': form, 'title': 'login'}
        return render(request, 'users/login.html', context)


@login_required
def profile_view(request):
    if request.method == "POST":
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = UserProfileUpdateForm(
            request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, "Your account has been updated")
        return redirect(reverse('profile'))
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = UserProfileUpdateForm(instance=request.user.profile)
        context = {'u_form': u_form, 'p_form': p_form, 'title': "Profile"}
        return render(request, 'users/profile.html', context=context)


@login_required
def logout_view(request):
    logout(request)
    return redirect(reverse('home'))
