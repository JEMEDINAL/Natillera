from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
import random
from django.core.exceptions import ValidationError

@login_required
def inicio(request):
    usuario_actual_dict = request.session.get('logueo', None)
    if usuario_actual_dict is not None:
        usuario_id = usuario_actual_dict.get('id', None)
        if usuario_id is not None:
            try:
                natillera_usuario = Natillera.objects.get(usuario=usuario_id)
                tiene_natillera = True
            except Natillera.DoesNotExist:
                tiene_natillera = False
        else:
            tiene_natillera = False
    else:
        tiene_natillera = False
    context = {'logueo': usuario_actual_dict, 'tiene_natillera': tiene_natillera}
    return render(request, "app/index.html", context)

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
            return redirect("iniciar")
    else:
        messages.warning(request, "Error: no se enviaron datos....")
        return redirect("iniciar")


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

@login_required
def crear_natillera(request):
    usuario_actual_dict = request.session.get('logueo', None)
    if usuario_actual_dict is None:
        return redirect('login')
    user_id = usuario_actual_dict.get('id', None)
    if user_id is not None:
        try:
            usuario_actual = User.objects.get(id=user_id)
        except User.DoesNotExist:
            messages.error(request, 'Usuario no encontrado')
            return redirect('crear_natillera')
    else:
        messages.error(request, 'ID de usuario no proporcionado en la sesión')
        return redirect('crear_natillera')
    
    if request.method == 'POST':
        nombre = request.POST.get('name')
        direccion = request.POST.get('address')
        telefono = request.POST.get('phone')
        periodicidad = request.POST.get('Periodicidad')
        numero = random.randint(1000,9999)
        codigo = numero
        try:
            new_natillera = Natillera(usuario=usuario_actual , nombre=nombre,
            direccion=direccion,telefono=telefono,periodicidad=periodicidad,
            codigo=codigo)
            new_natillera.save()
            messages.success(request, 'Registro exitoso. Ahora puedes usar tu natillera.')
            context = {'logueo': usuario_actual}
            return render(request, 'app/index.html', context)
        except ValidationError as e:
            messages.error(request, 'Registro de natillera inválido')
            return redirect('crear_natillera')
    context = {'logueo': usuario_actual }
    return render(request, 'app/menu_natillera/crear_natillera.html', context)


@login_required
def nati_usuario(request):
    usuario_actual_dict = request.session.get('logueo', None)
    if usuario_actual_dict is not None:
        usuario_id = usuario_actual_dict.get('id', None)
        if usuario_id is not None:
            try:
                natillera_usuario = Natillera.objects.get(usuario=usuario_id) # aca obtenemos lo que tiene usuario como natillera
                tiene_natillera = True
            except Natillera.DoesNotExist:
                tiene_natillera = False
        else:
            tiene_natillera = False
    else:
        tiene_natillera = False
   
    context ={'logueo': usuario_actual_dict,'nati_usuario': natillera_usuario , 'tiene_natillera': tiene_natillera}
    return render(request, 'app/menu_natillera/elige_natillera.html',context)


@login_required
def personas_y_socios(request, natillera_id):
    usuario_actual_dict = request.session.get('logueo', None)
    natillera = Natillera.objects.get(id=natillera_id)
    
    # Puedes agregar más lógica aquí según tus necesidades
    
    context = {'natillera': natillera, 'logueo': usuario_actual_dict}
    return render(request, 'app/menu_natillera/persona_socios.html', context)
