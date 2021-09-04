from django.shortcuts import render, redirect, HttpResponse
from django.http import JsonResponse
from django.contrib import messages
import bcrypt
from .models import User, Message, Comment

def index(request):
    context = {
        'saludo': 'Hola'
    }
    return render(request, 'index.html', context)



def register(request):

    if request.method == 'GET':
        return render(request, 'register.html')

    else:
        name = request.POST['name']
        email = request.POST['email']
        password = request.POST['password']
        password_conf = request.POST['password_conf']

        #validar el formulario:
        errors = User.objects.basic_validator(request.POST)
        if len(errors) >0:
            for llave, mensaje_de_error in errors.items():
                messages.error(request, mensaje_de_error)

            return redirect('/register')

        #verificar que ambas contraseñas sean iguales:
        if password != password_conf:
            messages.error(request,"Las contraseñas no coinciden")
            return redirect('/register')

    #se crea un usuario nuevo
    user = User.objects.create(
        name=name,
        email=email,
        password=bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    )

    #se guarda el usuario en sesión
    request.session['user'] = {
        'id': user.id,
        'name' : user.name,
        'email' : user.email,
        'avatar' : user.avatar
    }
    return redirect('/wall')


def login(request):

    email = request.POST['email']
    password = request.POST['password']
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist: 
        messages.error(request, 'El usuario no existe o contraseña erronea')
        return redirect('/register')

    if not bcrypt.checkpw(password.encode(), user.password.encode()):
        messages.error(request, 'El usuario no existe o contraseña erronea')
        return redirect('/register')

    #se confirma usuario y contraseña correcta

    request.session['user'] = {
        'id': user.id,
        'name' : user.name,
        'email' : user.email,
        'avatar' : user.avatar
    }
    return redirect('/wall')

def logout(request):
    request.session['user'] = None
    messages.success(request, f'¡Nos vemos!')

    return redirect('/register')



def wall(request):
    messages = Message.objects.all().order_by('-updated_at')
    comments = Comment.objects.all()
    users = User.objects.all()


    context = {
        'messages': messages,
        'comments': comments,
        'users': users
    }

    return render(request, 'wall.html', context)

def new_post(request):
    message = request.POST['message']

    message = Message.objects.create(
    message = message, 
    user_id = request.session['user']['id'])

    messages.success(request, f'El mensaje ha sido publicado')

    return redirect('/wall')


def comment(request):
    comment = request.POST['comment']

    comment = Comment.objects.create(
        comment=comment,
        user_id = request.session['user']['id'])

    return redirect('/wall')



