from django.db import models
from django.contrib.auth.models import AbstractUser
import qrcode
from io import BytesIO
import os
from PIL import Image, ImageDraw, ImageFont
from django.core.files.base import ContentFile
from django.utils import timezone
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from django.db.models import Q





class User(AbstractUser):
    #groups = models.ManyToManyField(
    #    'auth.Group', related_name='custom_user_groups', blank=True
    #)
    groups = models.ManyToManyField(Group, related_name='custom_user_groups', blank=True)
    #user_permissions = models.ManyToManyField(Permission, related_name='custom_user_permissions', blank=True)
    user_permissions = models.ManyToManyField(
        'auth.Permission', related_name='custom_user_permissions', blank=True
    )
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('soporte', 'Soporte'),
        ('operador', 'Operador'),
    ]
    #role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='operador')
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='operador')
    date_of_birth = models.DateField(null=True, blank=True)  # Fecha de nacimiento
    phone_number = models.CharField(max_length=15, null=True, blank=True)  # Teléfono
    address = models.TextField(null=True, blank=True)  # Dirección
    permissions = models.TextField(null=True, blank=True)  # Permisos personalizados

    def __str__(self):
        return f"{self.username} - {self.role}"

#User = get_user_model()

class Item(models.Model):
    ESTADO_CHOICES = [
        ('inicial', 'masterizado'),
        ('desplegado', 'desplegado'),
         ('pendiente', 'Pendiente'),
         ('en_progreso', 'En Progreso'),
        ('completado', 'Completado'),
        ('backup', 'backup'),
        ('transmitido', 'transmitido'),
    ]
    #fecha_actualizacion = models.DateTimeField(default=timezone.now)
    nombre = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    cont_R = models.CharField(max_length=50, blank=True, null=True)
    cont_C = models.CharField(max_length=50, blank=True, null=True)
    #estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='inicial')
    estado = models.CharField(
        max_length=20,
        choices=[('inicial', 'masterizado'), ('pendiente', 'Pendiente'), ('en_progreso', 'En Progreso'), ('completado', 'Completado'), ('backup', 'backup'), ('transmitido', 'transmitido') , ],
        default='inicial'
    )
    soporte = models.ForeignKey(User, related_name='soporte_items', on_delete=models.SET_NULL, null=True, blank=True)
    #asignado_a = models.ForeignKey(User, related_name='operador_items', on_delete=models.SET_NULL, null=True, blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    ticket_id = models.CharField(max_length=20, unique=True, blank=True)

    asignado_a = models.ForeignKey(User, related_name='operador_tickets', on_delete=models.SET_NULL, null=True, blank=True, limit_choices_to={'role': 'operador'})
    seguimiento_por = models.ForeignKey(User, related_name='soporte_tickets', on_delete=models.SET_NULL, null=True, blank=True, limit_choices_to={'role': 'soporte'})
    #fecha_creacion = models.DateTimeField(auto_now_add=True)
    codigo_qr = models.ImageField(upload_to='qrcodes/', blank=True, null=True)

 
    
    
    def generate_qr_code(self):
        """Genera un código QR basado en el ticket_id."""
        qr = qrcode.make(f"Estacion: {self.ticket_id}\n"
                         f"R: {self.cont_R}    C:{self.cont_C}\n"
                         f"asignado: {self.asignado_a}\n"
                         f"M por: {self.seguimiento_por}\n"
                         f"http://127.0.0.1:8000/api/items/{self.id}/")
        
        qr_image = qr.convert('RGB')

        # Crear una imagen de fondo donde se agregará el QR y el texto
        width, height = qr_image.size
        image = Image.new('RGB', (width, height + 50), color=(255, 255, 255))  # Agregar espacio para el texto

        # Pegar el QR en la imagen nueva
        image.paste(qr_image, (0, 0))

        # Crear un objeto de dibujo para agregar texto
        draw = ImageDraw.Draw(image)

        # Usar una fuente predeterminada o una fuente personalizada
        try:
            font = ImageFont.truetype("arial.ttf", 22)  # Cambiar a una fuente más grande o personalizada
        except IOError:
            font = ImageFont.load_default()  # Fuente predeterminada si no se encuentra la fuente

        # Definir el texto a agregar
        text = f"Estacion: {self.ticket_id} R: {self.cont_R} C:{self.cont_C}\n Asignado a: {self.asignado_a}"

        # Obtener el tamaño del texto utilizando textbbox
        text_bbox = draw.textbbox((0, 0), text, font=font)
        text_width = text_bbox[2] - text_bbox[0]  # Ancho del texto
        text_height = text_bbox[3] - text_bbox[1]  # Altura del texto

        # Definir la posición del texto (centrado horizontalmente debajo del QR)
        text_position = ((width - text_width) // 2, height - 5)  # Centrar horizontalmente y ponerlo debajo del QR

        # Agregar el texto
        draw.text(text_position, text, fill=(0, 0, 0), font=font)

        #qr_path = f"qrcodes/{self.ticket_id}_qr.png"  # Ruta donde debería guardarse
        #qr.save(qr_path)  # Guardar localmente
        qr_path = f"qrcodes/{self.ticket_id}.png"
        image.save(qr_path)  # Guardar la imagen localmente

        print(f"Código QR generado: {os.path.abspath(qr_path)}") 

        buffer = BytesIO()
        qr.save(buffer, format="PNG")
        self.codigo_qr.save(f"qr_{self.ticket_id}.png", ContentFile(buffer.getvalue()), save=False)
        #super().save(update_fields=['qr_code'])
       
    def save(self, *args, **kwargs):
        self.generate_qr_code()  # Generar QR antes de guardar
        super().save(*args, **kwargs)
    def __str__(self):
        return self.ticket_id      


class Complemento(models.Model):
    item = models.ForeignKey(Item, related_name="complementos", on_delete=models.CASCADE)
    nombre = models.CharField(max_length=255)
    precio_adicional = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.nombre} - {self.item.nombre}"
#class CustomUser(AbstractUser):
#    date_of_birth = models.DateField(null=True, blank=True)
#    phone_number = models.CharField(max_length=15, null=True, blank=True)
#    address = models.CharField(max_length=255, null=True, blank=True)
    # Add any other custom fields

    def __str__(self):
        return self.username
    
