from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
from django.http.response import JsonResponse
from django.core.serializers import serialize
import random
from django.core.exceptions import ValidationError


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
        try:
            user = User(nombre=nombre,apellido=apellido,correo=correo,clave=clave1)
            user.save()
            messages.success(request, 'Registro exitoso. Ahora puedes iniciar sesión.')
            return redirect('iniciar')
        except Exception as e:
            messages.error(request, f'Error al registrar usuario')
            return redirect('Registrarse')

    return render(request, 'app/sing_up.html')


def crear_natillera(request):
    usuario_actual_dict = request.session.get('logueo', None)
    if usuario_actual_dict == None :
        return render(request, 'app/index.html')
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



def nati_usuario(request):
    usuario_actual_dict = request.session.get('logueo', None)
    if usuario_actual_dict == None :
        return render(request, 'app/index.html')
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


def propiedad_natillera(request, natillera_id):
    usuario_actual_dict = request.session.get('logueo', None)
    if usuario_actual_dict == None :
        return render(request, 'app/index.html')
    natillera = Natillera.objects.get(id=natillera_id)
    context = {'natillera': natillera, 'logueo': usuario_actual_dict}
    return render(request, 'app/menu_natillera/administracion_nati.html', context)



def json_personas(request):
    usuario_actual_dict = request.session.get('logueo', None)
    if usuario_actual_dict == None :
        return render(request, 'app/index.html')
    if usuario_actual_dict is not None:
        usuario_id = usuario_actual_dict.get('id', None)
        if usuario_id is not None:
            try:
                natillera_usuario = Natillera.objects.get(usuario=usuario_id)
                tiene_natillera = True
            except Natillera.DoesNotExist:
                tiene_natillera = False
    natillera_id = natillera_usuario.id 
    natillera = Natillera.objects.get(id=natillera_id)
    personas = Persona.objects.filter(natillera=natillera)
    lista_personas = lista_personas = [{'nombre': persona.nombre, 'apellido': persona.apellido,'codigo': persona.codigo} for persona in personas]
    data = {'personas': lista_personas}
    return JsonResponse(data)

def json_socio(request):
    usuario_actual_dict = request.session.get('logueo', None)
    if usuario_actual_dict == None :
        return render(request, 'app/index.html')
    if usuario_actual_dict is not None:
        usuario_id = usuario_actual_dict.get('id', None)
        if usuario_id is not None:
            try:
                natillera_usuario = Natillera.objects.get(usuario=usuario_id)
                tiene_natillera = True
            except Natillera.DoesNotExist:
                tiene_natillera = False
    natillera_id = natillera_usuario.id 
    natillera = Natillera.objects.get(id=natillera_id)
    socios = Socio.objects.filter(natillera=natillera)
    lista_socios = [{'id':socio.id,'nombre': socio.nombre, 'apellido': socio.apellido,'codigo': socio.codigos,'ciclo':socio.periodicidad,'cuota':socio.cuota} for socio in socios]
    data = {'socios': lista_socios}
    return JsonResponse(data)



def personas_crear(request):
    usuario_actual_dict = request.session.get('logueo',None)
    if usuario_actual_dict == None:
        return render(request, 'app/index.html')
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        apellido = request.POST.get('apellido')
        numero = random.randint(10000000,99999999)
        natillera_id = request.POST.get('natillera')
        codigo = numero
        natillera = Natillera.objects.get(id=natillera_id)
        try:
            nueva_pesona = Persona(natillera=natillera , nombre=nombre,
            apellido=apellido,codigo=codigo)
            nueva_pesona.save()
            messages.success(request, 'Registro exitoso.')
            return redirect('propiedad_natillera', natillera_id)
        except ValidationError as e:
            messages.error(request, 'Registro inválido')
            return redirect('propiedad_natillera', natillera_id)
        

def socio_crear(request):
    usuario_actual_dict = request.session.get('logueo',None)
    if usuario_actual_dict == None:
        return render(request, 'app/index.html')
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        apellido = request.POST.get('apellido')
        periodicidad = request.POST.get('periodicidad')
        cuota = request.POST.get('cuota')
        cuota = cuota.replace('.', '').replace(',', '.')
        natillera_id = request.POST.get('natillera')
        numero = random.randint(10000000,99999999)
        codigo = numero
        personas_nati_actual = Persona.objects.filter(nombre=nombre,apellido=apellido)
        natillera = Natillera.objects.get(id=natillera_id)
        if personas_nati_actual.exists():
            primera_persona = personas_nati_actual.first()
            if primera_persona.nombre.lower() and primera_persona.apellido.lower() == nombre.lower() and apellido.lower():
                messages.error(request, "ya hay una persona igual de le en la flcha para convertirlo en socio a esta persona")
        else:
            nuevo_socio = Socio(natillera=natillera,nombre=nombre,apellido=apellido,codigos=codigo,periodicidad=periodicidad,cuota=cuota,activo=True)
            nueva_persona = Persona(natillera=natillera,nombre=nombre,apellido=apellido,codigo=codigo)
            nueva_persona.save()
            nuevo_socio.save()
            messages.success(request, 'Registro exitoso.')
    return redirect('propiedad_natillera', natillera_id)
        
            
       

