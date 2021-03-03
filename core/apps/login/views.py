from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render, reverse
from django.contrib import messages

from .forms import CreateUserForm


def registerPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        form = CreateUserForm()
        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                username = request.POST.get('username')
                password = request.POST.get('password1')
                if username and password:
                    user = authenticate(
                        request, username=username, password=password)
                    if user is not None and user.is_active and user.check_password:
                        login(request, user)
                        return redirect('home')
                return redirect(reverse('login'))
        context = {'form': form}
        return render(request, 'register.html', context)


def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        if username and password:
            user = authenticate(
                request, username=username, password=password)
            if user is not None and user.is_active and user.check_password:
                login(request, user)
                messages.success(request, 'Bienvenido' +
                                 username + '!')
                if 'next' in request.GET:
                    next_page = request.GET['next']
                    return redirect(next_page)
                return redirect('home')
            else:
                messages.warning(
                    request, 'Usuario o Password incorrectos..!')
                return render(request, "login.html")
    context = {}
    return render(request, 'login.html', context)


def logoutUser(request):
    logout(request)
    return redirect('/')