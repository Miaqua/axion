from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm, TaskForm, ProjectForm
from django.http import HttpResponseForbidden
from .models import Profile, Project, Task


def register_view(request):
    form = RegisterForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            user = form.save()

            Profile.objects.create(
            user=user,
            role='junior'
        )

            return redirect('login')

    return render(
        request,
        'register.html',
        {'form': form}
    )


def login_view(request):
    error = ''

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user:
            login(request, user)
            return redirect('index')
        else:
            error = 'Неверный логин или пароль'

    return render(
        request,
        'login.html',
        {'error': error}
    )


def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def index(request):
    update_overdue_tasks()
    
    projects_count = Project.objects.count()
    tasks_count = Task.objects.count()
    completed_tasks = Task.objects.filter(status='Завершена').count()
    in_progress_tasks = Task.objects.filter(status='В работе').count()
    overdue_tasks = Task.objects.filter(status='Просрочена').count()

    return render(
        request,
        'index.html',
        {
            'projects_count': projects_count,
            'tasks_count': tasks_count,
            'completed_tasks': completed_tasks,
            'in_progress_tasks': in_progress_tasks,
            'overdue_tasks': overdue_tasks,  
        }
    )


def update_overdue_tasks():
    tasks = Task.objects.exclude(status='Завершена')
    for task in tasks:
        task.update_overdue_status()


@login_required
def projects(request):
    projects = Project.objects.all()

    return render(
        request,
        'projects.html',
        {'projects': projects}
    )


@login_required
def project_detail(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    tasks = Task.objects.filter(project=project)
    for task in tasks:
        task.update_overdue_status()
    completed_tasks = tasks.filter(status='Завершена').count()
    
    return render(
        request,
        'project_detail.html',
        {
            'project': project,
            'tasks': tasks,
            'completed_tasks': completed_tasks
        }
    )


@login_required
def tasks(request):
    update_overdue_tasks()

    profile, created = Profile.objects.get_or_create(
        user=request.user,
        defaults={
            'role': 'junior'
        }
    )

    if profile.role == 'junior':
        tasks = Task.objects.filter(priority='Низкая')
    else:
        tasks = Task.objects.all()

    return render(
        request,
        'tasks.html',
        {'tasks': tasks}
    )




@login_required
def profile_view(request):
    update_overdue_tasks()

    profile, created = Profile.objects.get_or_create(
        user=request.user,
        defaults={
            'role': 'junior'
        }
    )

    my_tasks = Task.objects.filter(assigned_to=request.user)
    
    active_tasks = my_tasks.filter(status='В работе')
    completed_tasks = my_tasks.filter(status='Завершена')
    overdue_tasks = my_tasks.filter(status='Просрочена')

    return render(
        request,
        'profile.html',
        {
            'profile': profile,
            'my_tasks': my_tasks,
            'active_tasks': active_tasks,
            'completed_tasks': completed_tasks,
            'overdue_tasks': overdue_tasks,  
        }
    )


@login_required
def accept_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    
    if task.is_overdue():
        task.status = 'Просрочена'
        task.save()
        return redirect('tasks')

    if not task.assigned_to and task.status != 'Просрочена':
        task.assigned_to = request.user
        task.status = 'В работе'
        task.save()

    return redirect('tasks')

@login_required
def change_task_status(request, task_id, status):
    task = get_object_or_404(Task, id=task_id)

    if task.assigned_to != request.user:
        return HttpResponseForbidden()
    
    if task.is_overdue():
        task.status = 'Просрочена'
        task.save()
        return redirect('profile')

    allowed_statuses = ['В работе', 'Завершена']

    if status in allowed_statuses:
        task.status = status
        task.save()

    return redirect('profile')