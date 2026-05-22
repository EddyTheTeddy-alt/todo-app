from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import Task


def loginpage(request):
    error = None
    if request.method == 'POST':
        a = request.POST.get('username')
        b = request.POST.get('password')
        c = authenticate(username=a, password=b)
        if c:
            login(request, c)
            return redirect('dashboard')
        error = 'Invalid username or password.'
    return render(request, 'login.html', {'error': error})

def register(request):
    error = None
    entered_username = ''
    entered_email = ''
    entered_phone = ''
    if request.method == 'POST':
        entered_username = request.POST.get('username', '').strip()
        entered_email = request.POST.get('email', '').strip()
        entered_phone = request.POST.get('phone', '').strip()
        password = request.POST.get('password', '').strip()
        confirm_password = request.POST.get('confirm_password', '').strip()

        if not entered_username or not password or not confirm_password:
            error = 'Please fill the required fields.'
        elif password != confirm_password:
            error = 'Passwords do not match.'
        elif User.objects.filter(username=entered_username).exists():
            error = 'Username already exists.'
        else:
            User.objects.create_user(username=entered_username, password=password, email=entered_email)
            return redirect('login')
    return render(request, 'register.html', {
        'error': error,
        'entered_username': entered_username,
        'entered_email': entered_email,
        'entered_phone': entered_phone,
    })

def dashboard(request):
    c = Task.objects.filter(user=request.user)
    error = None
    if request.method == 'POST' and request.POST.get('todo_id'):
        todo = get_object_or_404(Task, id=request.POST.get('todo_id'), user=request.user)
        todo.status = request.POST.get('completed') == 'on'
        todo.save()
        return redirect('dashboard')
    if request.method == 'POST':
        a = request.POST.get('task', '').strip()
        b = request.POST.get('due_date', '').strip()
        d = request.POST.get('description')
        e = request.POST.get('status') == 'on'
        if not a or not b:
            error = 'Task and due date are required.'
        else:
            Task.objects.create(user=request.user, task=a, due_date=b, description=d, status=e)
            return redirect('dashboard')
    return render(request, 'dashboard.html', {'c': c, 'error': error})
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
    error = None
    if request.method == 'POST':
        task_name = request.POST.get('task', '').strip()
        due_date = request.POST.get('due_date', '').strip()
        description = request.POST.get('description', '')
        if not task_name or not due_date:
            error = 'Task and due date are required.'
        else:
            task.task = task_name
            task.due_date = due_date
            task.description = description
            task.status = request.POST.get('status') == 'on'
            task.save()
            return redirect('dashboard')
    return render(request, 'update.html', {'task': task, 'error': error})
