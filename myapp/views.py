from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import Task


def loginpage(request):
    if request.method == 'POST':
        a = request.POST.get('username')
        b = request.POST.get('password')
        c = authenticate(username=a, password=b)
        if c:
            login(request, c)
            return redirect('dashboard')
    return render(request, 'login.html')

def register(request):
    if request.method == 'POST':
        d = request.POST.get('username')
        e = request.POST.get('password')
        User.objects.create_user(username=d, password=e)
        return redirect('login')
    return render(request, 'register.html')

def dashboard(request):
    c = Task.objects.filter(user=request.user)
    if request.method == 'POST' and request.POST.get('todo_id'):
        todo = get_object_or_404(Task, id=request.POST.get('todo_id'), user=request.user)
        todo.status = request.POST.get('completed') == 'on'
        todo.save()
        return redirect('dashboard')
    if request.method == 'POST':
        a = request.POST.get('task')
        b = request.POST.get('due_date')
        d = request.POST.get('description')
        e = request.POST.get('status') == 'on'
        Task.objects.create(user=request.user, task=a, due_date=b, description=d, status=e)
        return redirect('dashboard')
    return render(request, 'dashboard.html', {'c': c})
def logout_view(request):
    logout(request)
    print('Logout successful')
    return redirect('login')

def delete_task(request,id):
    task=Task.objects.get(id=id)
    task.delete()
    return redirect('dashboard')

def edit_task(request,id):
    task=Task.objects.get(id=id)
    if request.method == 'POST':
        task.task=request.POST.get('task')
        task.due_date=request.POST.get('due_date')
        task.description=request.POST.get('description')
        task.status=request.POST.get('status') == 'on'
        task.save()
        return redirect('dashboard')
    return render(request, 'update.html', {'task': task})
