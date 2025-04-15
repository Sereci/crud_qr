from django.shortcuts import render, redirect
from django.contrib.auth.decorators import user_passes_test, login_required
from django.contrib.auth import logout
from django.contrib.auth import authenticate, login
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from rest_framework import viewsets, permissions
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import serializers
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from .serializers import UserSerializer
from .permissions import IsAdminOrReadOnly
from .models import Item
from .models import Item, Complemento, User  # <- Aquí arriba junto a los otros imports
from .serializers import UserSerializer, ItemSerializer, ComplementoSerializer

from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
import json
#from .models import Item
import os
from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A5
from reportlab.lib.units import mm
from reportlab.lib.units import cm
from django.conf import settings
from .models import Item
from django.http import FileResponse, Http404
from reportlab.lib.pagesizes import letter
#
def custom_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        print(f"Intentando iniciar sesión con: {username} - {password}")  # <-- Depuración
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            print(f"Autenticación exitosa para: {user.username}")  # <-- Depuración
           
            login(request, user)
            return redirect('dashboard')  # Redirige al dashboard después de iniciar sesión
        else:
            print("Autenticación fallida")  # <-- Depuración
           
            return render(request, 'login.html', {'error': 'Usuario o contraseña incorrectos'})
    
    return render(request, 'login.html')
@csrf_exempt
@login_required
def dashboard(request):
    request.user.refresh_from_db()
    role = getattr(request.user, 'role', None)
    print(f"Rol del usuario: {role}")
    """ Redirige a cada usuario según su rol """
    userepleLPOCr = request.user

    if request.user.role == "operador":
        return redirect('dashboard_operador')
    elif request.user.role == "soporte":
        return redirect('dashboard_soporte')
    elif request.user.role == "admin":
        return redirect('dashboard_admin')
    else:
        logout(request)
        return redirect('login')

@login_required
def dashboard_operador(request):
    """ Vista para operadores: muestra tareas asignadas """
    tareas = Item.objects.filter(asignado_a=request.user)
    return render(request, "dashboard_operador.html", {"tareas": tareas})

@login_required
def dashboard_soporte(request):
    """ Vista para soporte: muestra tareas que debe supervisar """
    tareas = Item.objects.filter(seguimiento_por=request.user)
    return render(request, "dashboard_soporte.html", {"tareas": tareas})

def es_superusuario(user):
    return user.is_superuser

#@login_required
#@user_passes_test(es_superusuario)
#def dashboard_admin(request):
#    """ Vista para administrador """
#    return render(request, "dashboard_admin.html")

@login_required
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])  # Solo usuarios autenticados pueden acceder
def dashboard_admin(request):
    """Vista para gestionar usuarios e ítems, accesible solo por superusuarios."""

    if not request.user.is_superuser:
        return JsonResponse({"error": "Acceso denegado"}, status=403)

    if request.method == 'GET':  
        users = User.objects.all()
        items = Item.objects.all()

        can_view_items = request.user.has_perm('app.view_item')
        can_view_users = request.user.has_perm('app.view_user')

        if 'application/json' in request.headers.get('Accept', ''):
            return Response({
                "usuarios": UserSerializer(users, many=True).data,
                "items": ItemSerializer(items, many=True).data
            })
        
        return render(request, 'dashboard_admin.html', {
            'items': items,
            'users': users,
            'can_view_items': can_view_items,
            'can_view_users': can_view_users,
        })

    elif request.method == 'POST':  
        if request.content_type == 'application/json':  
            if "username" in request.data:  
                serializer = UserSerializer(data=request.data)
            else:
                serializer = ItemSerializer(data=request.data)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return JsonResponse({"error": "Formato no soportado"}, status=400)

#@login_required
#def dashboard_soporte(request):
#    tareas = Item.objects.filter(seguimiento_por=request.user)  # Filtra tareas asignadas al soporte
#    return render(request, "dashboard_soporte.html", {"tareas": tareas})

def custom_logout(request):
        logout(request)
        return redirect('login')
    

#@csrf_exempt
@login_required
def actualizar_estado_tarea(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        tarea_id = data.get('tarea_id')
        nuevo_estado = data.get('nuevo_estado')

        try:
            tarea = Item.objects.get(id=tarea_id, seguimiento_por=request.user)
            tarea.estado = nuevo_estado
            tarea.save()
            return JsonResponse({'success': True, 'message': 'Estado actualizado'})
        except Item.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Tarea no encontrada'})
    
    return JsonResponse({'success': False, 'message': 'Método no permitido'})

def cambiar_estado(request, item_id, nuevo_estado):
    tarea = get_object_or_404(Item, id=item_id, asignado_a=request.user)
    tarea.estado = nuevo_estado
    tarea.save()
    return redirect('dashboard')

def solicitar_soporte(request, item_id):
    tarea = get_object_or_404(Item, id=item_id, asignado_a=request.user)
    tarea.estado = 'esperando_soporte'
    tarea.save()
    return redirect('dashboard')

class UserViewSet(viewsets.ModelViewSet):
    queryset = get_user_model().objects.all()
    #queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminOrReadOnly]

    def perform_create(self, serializer):
        """Asigna una contraseña encriptada al crear un usuario"""
        user = serializer.save()
        if 'password' in self.request.data:
            user.set_password(self.request.data["password"])  # Encripta la contraseña antes de guardarla
            user.save()


class ItemViewSet(viewsets.ModelViewSet):
    #queryset = Item.objects.all()
    #serializer_class = ItemSerializer
    #authentication_classes = [TokenAuthentication]
    #permission_classes = [IsAdminOrReadOnly]
    #def perform_update(self, serializer):
    #    """Permite actualizar el estado del ticket y regenerar el QR si es necesario"""
    #    item = serializer.save()
    #    if 'estado' in self.request.data:
    #        item.generate_qr_code()  # Regenera el QR si cambia el estado    
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminOrReadOnly]

    def update(self, request, *args, **kwargs):
        """Permite actualizar estado, soporte y operador"""
        item = self.get_object()
        estado = request.data.get("estado")
        asignado_a_id = request.data.get("asignado_a")
        seguimiento_por_id = request.data.get("seguimiento_por")

        # Validar estado
        ESTADOS_VALIDOS = ['pendiente', 'en_progreso', 'completado']
        if estado and estado not in ESTADOS_VALIDOS:
            return Response({"error": "Estado inválido"}, status=status.HTTP_400_BAD_REQUEST)
        
        # Validar y asignar operador (asignado_a)
        if asignado_a_id:
            try:
                asignado_a = User.objects.get(id=asignado_a_id)
                item.asignado_a = asignado_a
            except User.DoesNotExist:
                return Response({"error": "El operador no existe"}, status=status.HTTP_400_BAD_REQUEST)

        # Validar y asignar soporte (seguimiento_por)
        if seguimiento_por_id:
            try:
                seguimiento_por = User.objects.get(id=seguimiento_por_id)
                item.seguimiento_por = seguimiento_por
            except User.DoesNotExist:
                return Response({"error": "El usuario de soporte no existe"}, status=status.HTTP_400_BAD_REQUEST)

        # Guardar los cambios
        if estado:
            item.estado = estado
        item.save()
        return Response(ItemSerializer(item).data)
    

# Serializador para usuarios
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'is_staff', 'is_superuser']

# Serializador para ítems
class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = '__all__'

class ComplementoViewSet(viewsets.ModelViewSet):
    queryset = Complemento.objects.all()
    serializer_class = ComplementoSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]  # Cualquier usuario autenticado puede agregar complementos

    def perform_create(self, serializer):
        """Solo soporte puede agregar complementos"""
        if self.request.user.role != 'soporte':
            raise PermissionDenied("Solo los usuarios de soporte pueden agregar complementos")
        serializer.save()   
 # listar todos los items        
def lista_items(request):
    items = Item.objects.all().order_by('-fecha_creacion')
    return render(request, 'app/lista_items.html', {'items': items})

#generar pdf
@user_passes_test(lambda u: u.is_staff)#solo usuarios staff
def generar_pdf_item_qr(request, item_id):
    try:
        item = Item.objects.get(id=item_id)
    except Item.DoesNotExist:
        raise Http404("Item no encontrado")

    # Ruta absoluta del archivo QR
    qr_filename = item.codigo_qr.name  # campo tipo ImageField
    print(qr_filename) # imprimir el nombre del
    qr_path = os.path.join(settings.MEDIA_ROOT, qr_filename)

    # Crear PDF en memoria configurar el tamaño 
    from io import BytesIO
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=A5)
    p.setFont("Helvetica-Bold", 25)
    #Dibuja texto
    #texto arriba
    #p.drawString(40, 430, f"Est: {item.ticket_id}   R: {item.cont_R}   C:{item.cont_C}")
    #p.drawString(40, 410, f"A: {item.asignado_a}")
     #texto medio
    #p.drawString(40, 250, f"Est: {item.ticket_id}   R: {item.cont_R}   C:{item.cont_C}")
    #p.drawString(40, 230, f"A: {item.asignado_a}")
     #texto abajo
    #p.drawString(40, 70, f"Est: {item.ticket_id}   R: {item.cont_R}   C:{item.cont_C}")
    #p.drawString(40, 50, f"A: {item.asignado_a}")
    #if os.path.exists(qr_path):
    if os.path.exists(qr_path):
        #Dibuja codigo
        p.drawImage(qr_path, 40, 462, width=120, height=120)
        p.drawImage(qr_path, 40, 282, width=120, height=120)
        p.drawImage(qr_path, 40, 92, width=120, height=120)
    else:
        p.drawString(100, 700, "QR no encontrado.")




    #texto arriba
    p.drawString(40, 442, f"{item.ticket_id}")
    
     #texto medio
    p.drawString(40, 262, f"{item.ticket_id}")
   
     #texto abajo
    p.drawString(40, 70, f"{item.ticket_id}")

    asignado_a = item.asignado_a if item.asignado_a else "..................."

    p.setFont("Helvetica-Bold", 11)
    p.drawString(100, 442, f"     R: {item.cont_R} C:{item.cont_C}")
    p.drawString(40, 426, f"A: {asignado_a}")
    p.drawString(40, 410, f"Equipo: {item.nombre}")

    p.drawString(100, 262, f"     R: {item.cont_R}   C:{item.cont_C}")
    p.drawString(40, 242, f"A: {asignado_a}")
    p.drawString(40, 226, f"Equipo: {item.nombre}")

    p.drawString(100, 70, f"      R: {item.cont_R}   C:{item.cont_C}")
    p.drawString(40, 52, f"A: {asignado_a}")
    p.drawString(40, 36, f"Equipo: {item.nombre}")
    
    p.showPage()
    p.save()

    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename=f'item_{item.id}_qr.pdf')

def item_detail_html(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    return render(request, 'app/item_detail.html', {'item': item})