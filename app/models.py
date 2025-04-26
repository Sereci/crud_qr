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
        ('coordi', 'Coordinador'),
        ('operador', 'Operador'),
        ('logistica', 'Logística'),
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
    nombre = models.CharField(max_length=100,verbose_name="Etiqueta")
    description = models.TextField(blank=True, null=True, verbose_name="Registro transmision")
    cont_R = models.CharField(max_length=50, blank=True, null=True)
    cont_C = models.CharField(max_length=50, blank=True, null=True)
    estado = models.CharField(
        max_length=20,
        choices=ESTADO_CHOICES,
        default='inicial'
    )
    soporte = models.ForeignKey(User, related_name='soporte_items', on_delete=models.SET_NULL, null=True, blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    ticket_id = models.CharField(max_length=20, unique=True, blank=True,verbose_name="Estacion")
    asignado_a = models.ForeignKey(User, related_name='operador_tickets', on_delete=models.SET_NULL, null=True, blank=True, limit_choices_to={'role': 'operador'})
    seguimiento_por = models.ForeignKey(User, related_name='coordi_tickets', on_delete=models.SET_NULL, null=True, blank=True, limit_choices_to={'role': 'coordi'})
    codigo_qr = models.ImageField(upload_to='qrcodes/', blank=True, null=True)

    def __str__(self):
        asignado = self.asignado_a.get_full_name() if self.asignado_a else "Sin asignar"
        return f"{self.ticket_id} - {asignado}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.generate_qr_code()
        super().save(update_fields=["codigo_qr"])

    def generate_qr_code(self):
        qr = qrcode.make(f"https://crud-qr.onrender.com/api/view/items/{self.id}/")
        qr_image = qr.convert('RGB')

        width, height = qr_image.size
        image = Image.new('RGB', (width, height + 50), color=(255, 255, 255))
        image.paste(qr_image, (0, 0))

        draw = ImageDraw.Draw(image)

        try:
            font = ImageFont.truetype("arial.ttf", 22)
        except IOError:
            font = ImageFont.load_default()

        text = f""
        text_bbox = draw.textbbox((0, 0), text, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        text_position = ((width - text_width) // 2, height - 5)
        draw.text(text_position, text, fill=(0, 0, 0), font=font)

        buffer = BytesIO()
        image.save(buffer, format="PNG")
        filename = f"qr_{self.ticket_id}.png"
        self.codigo_qr.save(filename, ContentFile(buffer.getvalue()), save=False)

 # Añadir clases oficina , historicoMovimiento, activo
class Oficina(models.Model):
    codigo = models.CharField(max_length=16, unique=True)
    nombre_de_la_oficina = models.CharField(max_length=250)
    ubicacion = models.CharField(max_length=250)
    georefenciacido = models.CharField(null=True,max_length=250,  blank=True)

    def __str__(self):
        return self.nombre_de_la_oficina


class HistoricoMovimiento(models.Model):
    fecha_de_llegada = models.DateField()
    responsable = models.ForeignKey(User, related_name='coordinador_tickets',
                                    on_delete=models.SET_NULL, null=True,
                                    limit_choices_to={'role': 'coordi'})
    item = models.ForeignKey(Item, related_name='historicos',
                             on_delete=models.SET_NULL, null=True, blank=True)
    oficina = models.ForeignKey(Oficina, related_name='oficina_tickets',
                                on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.item} - {self.fecha_de_llegada}"


class Activo(models.Model):
    TIPO_EQUIPO_CHOICES = [
        ('fijo', 'Fijo'),
        ('movil', 'Movil'),
    ]
    item = models.ForeignKey(Item, related_name='activos',
                             on_delete=models.SET_NULL, null=True, blank=True)
    tipo_de_equipo = models.CharField(max_length=10, choices=TIPO_EQUIPO_CHOICES)
    maleta = models.CharField(max_length=50, blank=True)
    laptop_y_cargador = models.CharField(max_length=50, blank=True)
    monitor_cable_vga_y_poder = models.CharField(max_length=50,blank=True)
    teclado_mouse = models.BooleanField(default=False)
    cpu_y_cable_de_poder = models.CharField(max_length=50,blank=True)
    decadactilar = models.CharField(max_length=50)
    escaner_y_usb = models.CharField(max_length=50)
    hub = models.CharField(max_length=50)
    estabilizador = models.CharField(max_length=50)
    camara_cargador_y_usb = models.CharField(max_length=50)
    impresora = models.CharField(max_length=50)
    banner = models.BooleanField(default=False)
    tripode = models.BooleanField(default=False)
    cable_de_extension = models.BooleanField(default=False)
    adaptador_3_a_1 = models.BooleanField(default=False)
    observacion = models.TextField(blank=True)

    def __str__(self):
        return f"{self.tipo_de_equipo} - Maleta: {self.maleta}"

    
    
def generate_qr_code(self):
    """Genera un código QR basado en el ticket_id del Item asociado."""
    if not self.item:
        return  # Evita errores si no hay item asignado

    qr = qrcode.make(f"https://crud-qr.onrender.com/api/view/items/{self.item.id}/")
    qr_image = qr.convert('RGB')

    # Crear una imagen de fondo donde se agregará el QR y el texto
    width, height = qr_image.size
    image = Image.new('RGB', (width, height + 50), color=(255, 255, 255))
    image.paste(qr_image, (0, 0))

    draw = ImageDraw.Draw(image)

    try:
        font = ImageFont.truetype("arial.ttf", 22)
    except IOError:
        font = ImageFont.load_default()

    #text = f"Estacion: {self.item.ticket_id} R: {self.item.cont_R} C:{self.item.cont_C}\nAsignado a: {self.item.asignado_a}"

    text_bbox = draw.textbbox((0, 0), text, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_position = ((width - text_width) // 2, height - 5)
    draw.text(text_position, text, fill=(0, 0, 0), font=font)

    qr_path = f"qrcodes/{self.item.ticket_id}.png"
    image.save(qr_path)

    print(f"Código QR generado: {os.path.abspath(qr_path)}")

    buffer = BytesIO()
    qr.save(buffer, format="PNG")
    self.codigo_qr.save(f"qr_{self.item.ticket_id}.png", ContentFile(buffer.getvalue()), save=False)


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
    
