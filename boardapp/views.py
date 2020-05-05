from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .models import BoardModel
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView
from django.urls import reverse_lazy

# Create your views here.

def signupfunc(request):
    if request.method == 'POST':
        wkUsername = request.POST['username']
        wkPassword = request.POST['password']
        try:
            User.objects.get(username=wkUsername)
            return render(request, 'signup.html', {'error':'このユーザーは登録されています'})
        except:
            user = User.objects.create_user(wkUsername, '',wkPassword)
            return render(request, 'signup.html', {'some':'somedata'})
    return render(request, 'signup.html', {'some':'somedata'})


def loginfunc(request):
    if request.method == 'POST':
        wkUsername = request.POST['username']
        wkPassword = request.POST['password']
        user = authenticate(request, username=wkUsername, password=wkPassword)
        if user is not None:
            login(request, user)
            return redirect('list')
        else:
            return redirect('login')
    return render(request, 'login.html')

@login_required
def listfunc(request):
    object_list = BoardModel.objects.all()
    return render(request, 'list.html', {'object_list': object_list})


def logoutfunc(request):
    logout(request)
    return redirect('login')


def detailfunc(request, pk):
    object = BoardModel.objects.get(pk=pk)
    return render(request, 'detail.html', {'object': object})


def goodfunc(request, pk):
    object = BoardModel.objects.get(pk=pk)
    object.good = object.good + 1
    object.save()
    return redirect('list')


def readfunc(request, pk):
    object = BoardModel.objects.get(pk=pk)
    post = request.user.get_username()
    if post in object.readtext:
        return redirect('list')
    else:
        object.read = object.read + 1
        object.readtext = object.readtext + ' ' + post
        object.save()
    return redirect('list')


class BoardCreate(CreateView):
    template_name = 'create.html'
    model = BoardModel
    fields = ('title', 'content', 'author', 'images')
    success_url = reverse_lazy('list')