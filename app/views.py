from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
from django.contrib.auth import authenticate, login

def inicio(request):
    return render(request, "app/index.html")
 
def iniciar_sesion(request):
    return render(request, "app/login.html")
    
def login(request):
    if request.method == 'POST':
        user = request.POST.get('correo')
        password = request.POST.get('clave')
        try:
            q = User.objects.get(correo=user, clave=password)
            request.session["logueo"] = {
                "id": q.id,
                "nombre": q.nombre,
                "apellido": q.apellido
            }
            context = {'logueo': request.session.get('logueo', None)}
            messages.success(request, f"Bienvenido: {q.nombre}")
            return render(request, 'app/index.html', context)
        except User.DoesNotExist:
            messages.error(request, "Error: Usuario o contraseña incorrectos....")
            return redirect("login")
    else:
        messages.warning(request, "Error: no se enviaron datos....")
        return redirect("login")


def logout(request):
	try:
		del request.session["logueo"]
		messages.success(request, "Sesión cerrada correctamente!")
		return redirect("inicio")
	except Exception as e:
		messages.warning(request, "No se pudo cerrar sesión...")
		return redirect("inicio")

def sign_up(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        apellido = request.POST.get('apellido')
        correo = request.POST.get('correo')
        clave1 = request.POST.get('clave')
        clave2 = request.POST.get('clave2')
        if clave1 != clave2:
            messages.error(request, 'Las contraseñas no coinciden.')
            return redirect('Registrarse')

        # Crear un nuevo usuario
        try:
            user = User(nombre=nombre,apellido=apellido,correo=correo,clave=clave1)
            user.save()
            messages.success(request, 'Registro exitoso. Ahora puedes iniciar sesión.')
            return redirect('iniciar')
        except Exception as e:
            messages.error(request, f'Error al registrar usuario')
            return redirect('Registrarse')

    return render(request, 'app/sing_up.html')
    
