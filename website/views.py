from audioop import tostereo
from django.shortcuts import render
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import user_passes_test
from django.http.response import JsonResponse
from django.contrib import messages
from django.urls import reverse
from website.models import ToDos

def isAuthenticated(user):
    return user.is_authenticated

# Create your views here.
def signin(request):
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request,username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('dashboard_url'))
        else:
            messages.error(request, 'Please enter a correct username and password. Note that both fields may be case-sensitive.')
            return HttpResponseRedirect(reverse('login_url'))

    return render(request, 'login.html')

def signout(request):
    logout(request)
    return HttpResponseRedirect(reverse('login_url'))

def signup(request):

    if request.POST:
        firstName = request.POST['firstName']
        lastName = request.POST['lastName']
        email = request.POST['email']
        username = request.POST['username']
        password = request.POST['password']

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already taken')
            return HttpResponseRedirect(reverse('signup_url'))
        else:
            user = User.objects.create_user(username, email, password)
            user.first_name = firstName
            user.last_name = lastName
            user.save()
            messages.success(request, 'Account created successfully')
            return HttpResponseRedirect(reverse('login_url'))            

    return render(request, 'signup.html')

@user_passes_test(isAuthenticated, login_url='login_url')
def dashboard(request):
    todos = ToDos.objects.filter(user = request.user, is_valid = True).all()
    context = {
        'todos': todos
    }
    return render(request, 'dashboard.html', context)
    
@user_passes_test(isAuthenticated, login_url='login_url')
def profile(request):
    if request.POST:
        firstName = request.POST['firstName']
        lastName = request.POST['lastName']
        email = request.POST['email']

        user = request.user
        user.first_name = firstName
        user.last_name = lastName
        user.email = email
        user.save()
        messages.success(request, 'Updated successfully')
        return HttpResponseRedirect(reverse('profile_url'))

    return render(request, 'profile.html')
    
@user_passes_test(isAuthenticated, login_url='login_url')
def updatePassword(request):
    if request.POST:
        password = request.POST['password']
        user = request.user
        user.set_password(password)
        user.save()
        messages.success(request, 'Updated successfully')
        return HttpResponseRedirect(reverse('updatePassword_url'))

    return render(request, 'updatePassword.html')

from django.views.decorators.csrf import csrf_exempt
import json
@csrf_exempt
@user_passes_test(isAuthenticated, login_url='login_url')
def addTodo(request):
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        todo = body['todo']
        todos = ToDos()
        todos.user = request.user
        todos.todo = todo
        todos.created_by = request.user
        todos.modified_by = request.user
        todos.save()
        return JsonResponse({'status': True, 'msg': '', 'id': todos.id}, status=200)

@csrf_exempt     
@user_passes_test(isAuthenticated, login_url='login_url')
def updateTodo(request):
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        id = body['id']
        todos = ToDos.objects.filter(id = id).first()
        todos.is_completed = False if todos.is_completed else True
        todos.modified_by = request.user
        todos.save()
        return JsonResponse({'status': True, 'msg': '', 'id': todos.id}, status=200)

@csrf_exempt     
@user_passes_test(isAuthenticated, login_url='login_url')
def deleteTodo(request):
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        id = body['id']
        todos = ToDos.objects.filter(id = id).first()
        todos.is_valid = False
        todos.modified_by = request.user
        todos.save()
        return JsonResponse({'status': True, 'msg': '', 'id': todos.id}, status=200)