from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from time import gmtime, strftime
from django.db.models import Count
import bcrypt

from .models import *

# Create your views here.
def inicio(request):
    if 'user_id' in request.session:
        return redirect('travels/')
    return render(request, 'registro.html')


def registrar(request):
    return render(request, 'registro.html')


def login(request):
    usuario = User.objects.filter(username=request.POST['ulogin'])
    errores = User.objects.validar_login(request.POST['plogin'], usuario)

    if len(errores) > 0:
        for key, msg in errores.items():
            messages.error(request, msg, extra_tags=key)
        return redirect('/')
    else:
        request.session['user_id'] = usuario[0].id
        request.session['user_name'] = usuario[0].name
        return redirect('travels/')


def registro(request):
    #validacion de parametros
    errors = User.objects.basic_validator(request.POST)

    if len(errors) > 0:
        for key, msg in errors.items():
            messages.error(request, msg, extra_tags=key)
        return redirect('/')

    else:
        #encriptar password
        password = User.objects.encriptar(request.POST['password'])
        

        #crear usuario
        user = User.objects.create(
            name=request.POST['name'],
            username=request.POST['username'].lower(),
            email=request.POST['email'].lower(),
            password=password,
        )
        #retornar mensaje de creacion correcta
        messages.success(request, "User successfully created!")
    return redirect('/')


def logout(request):
    request.session.flush()
    return redirect('/')


def change(request):
    return render(request, 'cambiar.html')


def cambiar_pass(request):
    reg_user = User.objects.filter(id=request.session['user_id'])
    errores = User.objects.validar_login(request.POST['actPass'], reg_user)
    
    if len(errores) > 0:
        for key, msg in errores.items():
            messages.error(request, msg, extra_tags=key)
        return render(request, 'cambiar.html')
    else:
        newPass = request.POST['newPass']
        confPass = request.POST['confPass']
        if len(newPass) < 8:
            messages.error(request, "New password should be at least 8 characters", extra_tags='newPass')
            return render(request, 'cambiar.html')

        mensaje = User.objects.comparar_password(newPass,confPass)
        if len(mensaje) > 0:
            messages.error(request, mensaje, extra_tags='confPass')
            return render(request, 'cambiar.html')
        
        password_encriptado = User.objects.encriptar(newPass)

        reg_user[0].password = password_encriptado
        reg_user[0].save()
        request.session.flush()
        messages.success(request, f"Password changed correctly, the session will be closed.")
        return render(request, 'cambiar.html')