from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from .forms import TareaForm
from .models import Tarea
from django.contrib.auth.decorators import login_required
from django.utils import timezone

# Create your views here.

def home(request):
        return render(request, 'home.html')
    
def signup(request):
    
    if request.method =='GET':
        return render(request, 'signup.html', {
            'form': UserCreationForm
        })
            
    else:
        if request.POST ['password1'] == request.POST['password2']:
            
            try:
                user= User.objects.create_user(username=request.POST ['username'],
                password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('tasks')
                
            except IntegrityError:
                return render(request, 'signup.html',{
                    'form': UserCreationForm,
                    'error': 'El usuario ya existe'
        })
        
        return render(request, 'signup.html',{
                    'form': UserCreationForm,
                    'error': 'Contraseña no coincide'
        })   

@login_required       
def tasks(request):
    tasks = Tarea.objects.filter(user=request.user, realizado__isnull=True)
    return render(request, 'tasks.html', {'tasks' : tasks})

@login_required    
def tasks_completed(request):
    tasks = Tarea.objects.filter(user=request.user, realizado__isnull=False) .order_by('-realizado')
    return render(request, 'tasks.html', {'tasks' : tasks})

@login_required        
def create_task(request):
    if request.method == 'GET':
        return render(request, 'create_task.html', {
            'form' : TareaForm
        })
    else:
        try:
            form = TareaForm(request.POST)
            if form.is_valid():
                nueva_tarea = form.save(commit=False)
                nueva_tarea.user = request.user
                nueva_tarea.save()
                return redirect('tasks')
            else:
                return render(request, 'create_task.html', {
                    'form': form,
                    'error': 'Formulario no válido. Corrige los errores.'
                })        
                       
        except ValueError:
            return render(request, 'create_task.html', {
                'form' : TareaForm,
                'error' : 'Por favor proporciona datos validos'
                })

@login_required         
def task_detail(request, task_id):
    task = get_object_or_404(Tarea, pk=task_id, user=request.user)    # Siempre se obtiene la tarea      
      
         
    if request.method == 'GET':
        form = TareaForm(instance=task)    # Inicializa el formulario con los datos actuales de la tarea
        return render(request, 'task_detail.html', {'task': task, 'form':form})
    else:
        try:     # Para solicitudes POST
            task = get_object_or_404(Tarea, pk=task_id, user=request.user)
            form = TareaForm(request.POST, instance=task) # Asocia los datos del formulario con la tarea existente
            if form.is_valid():  # Verifica si el formulario es válido
                form.save()          # Guarda los cambios en la tarea
            return redirect('tasks')     # Redirige a la lista de tareas
        except ValueError:               # Captura errores en la validación del formulario
            return render(request, 'task_detail.html', 
                {'task': task,
                'form':form,
                'error' : "Error actualizando tarea"
                })
@login_required                
def complete_task(request, task_id):
    task = get_object_or_404(Tarea, pk=task_id, user=request.user)
    if request.method == "POST":
        task.realizado = timezone.now()
        task.save()
        return redirect('tasks')

@login_required        
def delete_task(request, task_id):
    task = get_object_or_404(Tarea, pk=task_id, user=request.user)
    if request.method == "POST":
        task.delete()
        return redirect('tasks')

@login_required            
def signout(request):
    logout(request)
    return redirect('home') 

def signin(request):
        if request.method == 'GET':
            return render(request, 'signin.html', {
            'form': AuthenticationForm
        }) 
        else:
            user= authenticate(request, username=request.POST['username'], password=request.POST
                ['password'])
            if user is None:
                return render(request, 'signin.html', {
            'form': AuthenticationForm,
            'error': 'Usuario o contraseña es incorrecta'
        }) 
            else:
                login(request, user)
                return redirect('tasks')
                
                   
            
            
   
        
