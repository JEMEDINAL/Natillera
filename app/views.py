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
    natillera = Natillera.objects.get(pk=natillera_id)
    socios = Socio.objects.filter(natillera=natillera)
    contador = 0
    for socio in socios:
        if socio.activo == True:
            contador += 1
    context = {'natillera': natillera, 'logueo': usuario_actual_dict,"activos":contador}
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
    lista_personas = lista_personas = [{'id': persona.id,'nombre': persona.nombre, 'apellido': persona.apellido,'codigo': persona.codigo} for persona in personas]
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
    lista_socios = [{'id':socio.id,'nombre': socio.nombre, 'apellido': socio.apellido,
                     'codigo': socio.codigos,'ciclo':socio.periodicidad,'cuota':socio.cuota,'activo':socio.activo} for socio in socios]
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
        argumento = request.POST.get('argumento')
        nombre = request.POST.get('nombre')
        apellido = request.POST.get('apellido')
        periodicidad = request.POST.get('periodicidad')
        cuota = request.POST.get('cuota')
        
        natillera_id = request.POST.get('natillera')
        numero = random.randint(10000000,99999999)
        codigo = numero
        personas_nati_actual = Persona.objects.filter(natillera=natillera_id)
        natillera = Natillera.objects.get(id=natillera_id)
        if personas_nati_actual.filter(nombre__iexact=nombre, apellido__iexact=apellido,natillera=natillera_id).exists() and argumento == 'boton':
            messages.error(request, "Ya hay una persona igual. Utiliza la flecha para convertirla en socio a esta persona")
        elif argumento == 'flecha':
            old_cod = request.POST.get('codigo')
            nuevo_socio = Socio(natillera=natillera,nombre=nombre,apellido=apellido,codigos=old_cod,periodicidad=periodicidad,cuota=cuota,activo=True)
            nuevo_socio.save()
            messages.success(request, 'Registro exitoso.')
        else:
            nuevo_socio = Socio(natillera=natillera,nombre=nombre,apellido=apellido,codigos=codigo,periodicidad=periodicidad,cuota=cuota,activo=True)
            nuevo_socio.save()
            nueva_persona = Persona(natillera=natillera,nombre=nombre,apellido=apellido,codigo=codigo)
            nueva_persona.save()
            messages.success(request, 'Registro exitoso.')
    return redirect('propiedad_natillera', natillera_id)
    
    
    
def propiedad_socio(request, socio_id):
    usuario_actual_dict = request.session.get('logueo',None)
    natillera  = Natillera.objects.get(usuario=usuario_actual_dict['id'])
    todo_socio = Socio.objects.get(pk=socio_id)
    context = {'todo_socio':todo_socio,'natillera':natillera}
    return render(request, 'app/menu_natillera/propiedades_socio.html',context)

def editar_socio(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        nombre = request.POST.get('nombre')
        apellido = request.POST.get('apellido')
        pais = request.POST.get('pais')
        natillera = request.POST.get('natillera')
        cuota = request.POST.get('cuota')
        correo = request.POST.get('correo')
        departamento = request.POST.get('departamento')
        periodicidad = request.POST.get('periodicidad')
        ciudad = request.POST.get('ciudad')
        celular = request.POST.get('celular')
        codigo = request.POST.get('codigo')
        id = request.POST.get('id')
        nati = Natillera.objects.get(pk=natillera)
        try:
            socio = Socio.objects.get(pk=id)
            persona = Persona.objects.get(codigo=codigo)
            persona.natillera = nati
            persona.nombre = nombre
            persona.apellido = apellido
            socio.nombre = nombre
            socio.apellido = apellido
            socio.periodicidad  = periodicidad
            socio.cuota  = cuota
            socio.pais  = pais
            socio.departamento  = departamento
            socio.ciudad  = ciudad
            socio.Celular  = celular
            socio.correo  = correo
            socio.save()
            persona.save()
            messages.success(request, "Socio actualizado correctamente")
            return redirect('propiedad_natillera',natillera)
        except Exception as e:
            messages.error(request, f"Error: {e}")
            return redirect('propiedad_natillera',natillera)
        
        
def socio_table(request):
    usuario_actual_dict = request.session.get('logueo',None)
    natillera  = Natillera.objects.get(usuario=usuario_actual_dict['id'])
    socios = Socio.objects.filter(natillera=natillera)
    context = {'usuario_actual_dict': usuario_actual_dict,"natillera": natillera,"socios":socios}
    return render(request, 'app/menu_natillera/socio_table.html',context)


def dar_couta(request, id_socio):
    usuario_actual_dict = request.session.get('logueo',None)
    natillera  = Natillera.objects.get(usuario=usuario_actual_dict['id'])
    socio = Socio.objects.get(pk=id_socio)
    context = {'usuario_actual_dict': usuario_actual_dict,"natillera":natillera,"socio":socio}
    return render(request, 'app/menu_natillera/form_cuota.html', context)


def dar_cuota_form(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        fecha = request.POST.get('fecha')
        total = int(request.POST.get('total'))
        nati = request.POST.get('natillera')
        socio = Socio.objects.get(pk=id)
        if total >= socio.cuota:
            try:
                socio.capital= total
                socio.fecha_cuota= fecha
                socio.save()
                messages.success(request, "Pago realizado")
                return redirect('propiedad_natillera',nati)
            except Exception as e:
                messages.error(request, f"Error: {e}")
                return redirect("dar_cuota",id)
        else:
            messages.error(request, "la cuota es menor")
            return redirect("dar_cuota",id)
       

