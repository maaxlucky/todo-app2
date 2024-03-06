from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.core.paginator import Paginator
from django.views.generic import ListView

from .models import Task
from .forms import TaskForm, LoginUserForm, RegisterUserForm


# What happends when user passes -1 OR 9999999999999999 instead of page number
# TODO: read about "early return"
def index(request):
    user = request.user
    if user not in User.objects.all():
        return render(request, 'todoapp/index.html')

    tasks = user.task_set.all().order_by('id')
    paginator = Paginator(tasks, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'user': user,
        'page_obj': page_obj,
    }

    return render(request, 'todoapp/index.html', context)

@login_required
def search_task(request):
    user = request.user
    search = request.GET.get('q', '')
    tasks = user.task_set.filter(title__contains=search).order_by('id')
    paginator = Paginator(tasks, 3)
    page_number = request.GET.get('page')
    page_search = paginator.get_page(page_number)
    context = {
        'page_search': page_search,
        'q': search,
    }

    return render(request, 'todoapp/search_task.html', context)


# REST style
# GET /tasks/add (render form)
# POST /tasks (handle form)
# GET /tasks/{taskId}/form (render editing form)
# PUT /tasks/{taskId} (handle task edit)
# DELETE /tasks/{taskId} (handle task deletion)

@login_required
def add_task(request):
    if request.method == 'POST':

        user_id = request.POST['user'] # Insecure because client can prentent to be another user (neven trust the client)
        title = request.POST['title'] # What happends if user sends 50MB of text in title? If title > 50 symbols return http 400

        description = request.POST['description']
        date = request.POST['due_date'] # check if past date is not accepted
        user = User.objects.get(pk=user_id)
        user.task_set.create(title=title, description=description, date=date)
        return redirect('todoapp:index')
    else:
        form = TaskForm()
        return render(request, 'todoapp/add_task.html', {'form': form})


# Prerender fields in form so that you don't have to check if it has been modified
@login_required
def edit_task(request, task_id):
    if request.method == 'POST':
        task = Task.objects.get(pk=task_id)
        if task.title != request.POST['title'] and request.POST['title'] != '':
            task.title = request.POST['title']
        if task.description != request.POST['description'] and request.POST['description'] != '':
            task.description = request.POST['description']
        if task.date != request.POST['date'] and request.POST['date'] != '':
            task.date = request.POST['date']
        # traditional way
        # if request.POST.get('isDone', False) == 'on':
        #     task.isDone = True
        # else:
        #     task.isDone = False
        print(request.POST)
        # We can just search in POST request with similar name
        # If checkbox is empty it's automatically is False
        # If checkbox is not checked it returns Null in body of request
        task.isDone = 'isDone' in request.POST
        task.save()
        return redirect('todoapp:index')
    else:
        task = Task.objects.get(pk=task_id)
        return render(request, 'todoapp/edit_task.html', {'task': task})


@login_required
def delete_task(request, task_id):
    if request.method == 'POST': # DELETE http method for delete
        Task.objects.get(pk=task_id).delete()
        return redirect('todoapp:index')
    else:
        tasks = Task.objects.all()
        return render(request, 'todoapp/index.html', {'tasks': tasks})


def login_user(request):
    if request.method == 'POST':
        form = LoginUserForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd['username'], password=cd['password'])

            if user and user.is_active:
                login(request, user)
        return redirect('todoapp:index')
    else:
        form = LoginUserForm()
    return render(request, 'todoapp/login.html', {'form': form})


def logout_user(request):
    logout(request)
    return redirect('todoapp:index')
    # we can return to main page, or give access only regirestrated users
    # tasks = Task.objects.all()
    # users = User.objects.all()
    # context = {
    #     'tasks': tasks,
    #     'users': users,
    # }
    # return render(request, 'index.html', context)


def register_user(request):
    if request.method == 'POST':
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = User.objects.create_user(username=cd['username'], password=cd['password'])
            user.save()
            login(request, user)
        return redirect('todoapp:index')
    else:
        form = RegisterUserForm()
    return render(request, 'todoapp/register.html', {'form': form})
