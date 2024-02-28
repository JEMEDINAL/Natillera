from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
from django.http.response import JsonResponse
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
                socio.capital += total
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

def calendario(request):
    usuario_actual_dict = request.session.get('logueo',None)
    natillera = Natillera.objects.get(usuario=usuario_actual_dict["id"])
    todos_eventos = Eventos.objects.filter(natillera=natillera)
    list_eventos=[{'id':eve.id,'titulo':eve.nombre_del_evento,'fecha': eve.fecha_inicio, 'descripcion': eve.descripcion} for eve in todos_eventos]
    contexto = {"natillera": natillera,'evento':list_eventos}
    return render(request, 'app/menu_natillera/calendario.html', contexto)

def crear_evento(request):
    usuario_actual_dict = request.session.get('logueo',None)
    natillera = Natillera.objects.get(usuario=usuario_actual_dict["id"])
    if request.method == 'POST':
        fecha = request.POST.get('fecha_evento')
        titulo = request.POST.get('titulo')
        descripcion = request.POST.get('descripcion')
        try:
            eve = Eventos(natillera=natillera,nombre_del_evento=titulo,fecha_inicio=fecha,descripcion=descripcion)
            eve.save()
            messages.success(request, "Evento agregado exitosamente")
            return redirect('calendario')
        except Exception as e:
            messages.error(request, f"Error: {e}")
            return redirect('calendario')

def eliminar_evento(request):
    if request.method == 'POST':
        id_evento = request.POST.get('evento')
        print(id_evento)
        try:
            q = Eventos.objects.get(pk=id_evento)
            q.delete()
            messages.success(request, "Evento eliminado correctamente!!")
            
        except Exception as e:
            messages.error(request, f"Error: {e}")
    
    return redirect('calendario')


def prestamos(request,socio_id):
    usuario_actual_dict = request.session.get('logueo',None)
    socio = Socio.objects.get(pk=socio_id)
    natillera = Natillera.objects.get(usuario=usuario_actual_dict["id"])
    if Prestamo.objects.filter(socio=socio).exists():
        messages.error(request,"Error:socio ya tiene un prestamo")
        return redirect('table_socio')
    else:
        contexto = {'natillera': natillera,'socio':socio}
        return render(request, 'app/menu_natillera/prestamos.html',contexto)

def crear_prestamos(request):
    usuario_actual_dict = request.session.get('logueo',None)
    if usuario_actual_dict == None :
        return render(request, 'app/index.html')
    else:
        
        if request.method == 'POST':
            tipos = str(request.POST.get('tipos_c'))
            s_id = request.POST.get("id")
            socio = Socio.objects.get(pk=s_id)
            if Prestamo.objects.filter(socio=socio).exists():
                messages.error(request,"Error:socio ya tiene un prestamo")
                return redirect('table_socio')
            else:
                if tipos == "cuotas":
                    des = request.POST.get("descripcion")
                    cuotas_elegidas = request.POST.getlist("cuota_dia")
                    cantidad = request.POST.get('cantidad')
                    pagara = request.POST.get('pagara')
                    cuota = request.POST.get('cuota')
                    try:
                        if cuotas_elegidas:
                            cuota_cantidad = cuotas_elegidas[0]
                        else:
                            tipo=tipos
                        pres = Prestamo(
                            socio=socio,
                            cantidad=cantidad,
                            deuda=pagara,
                            cuota=cuota,
                            cantidad_cuotas=cuota_cantidad,
                            nota_o_descripcion=des,
                            tipo_pretamo=tipos
                            )
                        pres.save()
                        messages.success(request,"Prestamo realizado")
                        return redirect('table_socio')
                    except Exception as e:
                        messages.error(request,f"Error: {e}")
                        return redirect('table_socio')
                elif tipos == 'paga diario':
                    cantidad_pd = request.POST.get('cantidad_pd')
                    pagara_pd = request.POST.get('pagara_pd')
                    cuota_pd = request.POST.get('cuota_pd')
                    cuota_dias_pd = request.POST.get('cuota_dias_pd')
                    try:
                        
                        prestamos_pd = Prestamo(
                            socio=socio,
                            cantidad=cantidad_pd,
                            deuda=pagara_pd,
                            cuota=cuota_pd,
                            cantidad_cuotas=cuota_dias_pd,
                            tipo_pretamo=tipos,
                            nota_o_descripcion="Paga diario"
                        )
                        prestamos_pd.save()
                        messages.success(request,"Prestamo Realizado")
                        return redirect('table_socio')
                    except Exception as e:
                        messages.error(request,f"Error: {e}")
                        return redirect('table_socio')
                elif tipos == "convencional":
                    cantidad_c = request.POST.get('cantidad_c')
                    plazo_c = request.POST.get('plazo_c')
                    pagara_c = request.POST.get('pagara_c')
                    cuota_mes_c = request.POST.get('cuota_mes_c')
                    try:
                        prestamos_c = Prestamo(
                            socio=socio,
                            cantidad=cantidad_c,
                            deuda=pagara_c,
                            cuota=cuota_mes_c,
                            cantidad_cuotas=plazo_c,
                            tipo_pretamo=tipos,
                            nota_o_descripcion="Paga diario"
                        )
                        prestamos_c.save()
                        messages.success(request,"Prestamo Realizado")
                        return redirect('table_socio')
                    except Exception as e:
                        messages.error(request,f"Error: {e}")
                        return redirect('table_socio')


def pagar_deuda(request,id_socio):
    usuario_actual_dict = request.session.get('logueo',None)
    socios = Socio.objects.get(pk=id_socio)
    pres = Prestamo.objects.get(socio=socios)
    nati = Natillera.objects.get(usuario=usuario_actual_dict["id"])
    context ={"natillera":nati,"socios":socios,"prestamos":pres}
    return render(request, "app/menu_natillera/form_pagar_p.html",context)

def pagar_pagar_deuda(request):
    if request.method == "POST":
        cuota = int(request.POST.get('cuota'))
        prestamo = request.POST.get('prestamo')
        pres = Prestamo.objects.get(pk=prestamo)
        try:
            pres.deuda -= cuota
            pres.cantidad_cuotas -= 1
            pres.save()
            messages.success(request, "Pago realizado")
            return redirect("table_socio")
        except Exception as e:
            messages.error(request,f"Error: {e}")
            return redirect("table_socio")
        
    