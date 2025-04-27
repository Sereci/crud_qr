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

class Transmision(models.Model):
    id_soporte = models.ForeignKey(
        User,
        related_name='transmisiones_realizadas',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        limit_choices_to={'role': 'soporte'},
        verbose_name="Soporte que realizó la transmisión"
    )
    id_estacion = models.ForeignKey(
        Item,
        related_name='transmisiones',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Estación asociada"
    )
    r_final = models.CharField(max_length=250, null=False)
    c_final = models.CharField(max_length=250, null=False)
    observaciones = models.TextField(blank=True, null=True)

    fecha_transmision = models.DateTimeField(default=timezone.now)

    def __str__(self):
        soporte_nombre = self.id_soporte.get_full_name() if self.id_soporte else "Sin Soporte"
        estacion = self.id_estacion.ticket_id if self.id_estacion else "Sin Estación"
        return f"Transmisión de {estacion} por {soporte_nombre} ({self.fecha_transmision.date()})"


class Soporte(models.Model):
    ACTIVIDAD_CHOICES = [
        ('config_equipo', 'Configuración de equipo'),
        ('config_usuario_nuevo', 'Configuración de Usuario Nuevo'),
        ('config_usuario', 'Configuración de Usuario'),
        ('config_red_internet', 'Configuración de Red/Internet (PROXY-IP)'),
        ('conexion_cableado', 'Conexión de cableado de red'),
        ('verificacion_cableado', 'Verificación de cableado de red'),
        ('inventario_logico_fisico', 'Inventario Lógico/Físico'),
        ('instalacion_programas_drivers', 'Instalación de Programas/Drivers'),
        ('soporte_ofimatica', 'Soporte de ofimática'),
        ('mantenimiento_hardware_software', 'Mantenimiento Hardware/Software'),
        ('instalacion_equipo', 'Instalación de equipo'),
        ('capacitacion_usuario', 'Capacitación al Usuario'),
        ('tareas_empadronamiento', 'Tareas de Empadronamiento'),
    ]

    LUGAR_CHOICES = [
        ('planta_baja', 'PLANTA BAJA'),
        ('piso_1', 'PISO - 1'),
        ('piso_2', 'PISO - 2'),
        ('piso_3', 'PISO - 3'),
        ('piso_4', 'PISO - 4'),
        ('piso_5', 'PISO - 5'),
        ('megacentro', 'Megacentro'),
        ('rural', 'Rural'),
        ('otro', 'Otro'),
    ]

    TIPO_CHOICES = [
        ('impresora', 'IMPRESORA'),
        ('multifuncional', 'MULTIFUNCIONAL'),
        ('plotter', 'PLOTTER'),
        ('scanner', 'SCANNER'),
        ('todo_en_uno', 'TODO EN UNO'),
        ('portatil', 'PORTATIL'),
        ('biometrico', 'BIOMETRICO'),
        ('pc_escritorio', 'PC DE ESCRITORIO'),
        ('datashow', 'DATASHOW'),
    ]

    MODELO_CHOICES = [
        ('laserjet_cp1525nw', 'LASERJET CP1525NW'),
        ('laserjet_2015dn', 'LASERJET 2015DN'),
        ('laserjet_1020', 'LASERTJET 1020'),
        ('scanjet_7500_flow', 'SCANJET 7500 FLOW'),
        ('laserjet_p3015', 'LASERJET P3015'),
        ('laserjet_2035dn', 'LASERJET 2035DN'),
        ('l_5590', 'L 5590'),
        ('laserjet_1320', 'LASERJET 1320'),
        ('enterprise_m608dn', 'ENTERPRISE M608DN'),
        ('laserjet_pro_400_color_mfp_m475dn', 'LASERJET PRO 400 COLOR MFP M475DN'),
        ('laserjet_cp1025nw', 'LASERJET CP 1025 NW'),
        ('lbp_3000', 'LBP 3000'),
        ('lbp_6000', 'LBP 6000'),
        ('laserjet_p1005', 'LASERJET P1005'),
        ('laserjet_4250u', 'LASERJET 4250u'),
        ('laserjet_m506', 'LASERJET M506'),
        ('color_laserjet_m651', 'COLOR LASERJET M651'),
        ('laserjet_m507', 'LASERJET M507'),
        ('laserjet_100_color_mfp175_nwu', 'LASERJET 100 COLOR MFP175 NWu'),
        ('laserjet_3005dn', 'LASERJET 3005DN'),
        ('laserjet_9050dn', 'LASERJET 9050DN'),
        ('laserjet_3800dn', 'LASERJET 3800DN'),
        ('l355', 'L355'),
        ('laserjet_enterprice_m606', 'LASERJET ENTERPRICE M606'),
        ('laserjet_color_mfp_m175_ncv', 'LASERJET COLOR MFP M175 NCV'),
        ('laserjet_pro_400_color_mfp_m375_m475', 'LASERJET PRO 400 COLOR MFP M375 M475'),
        ('color_laserjet_cm2320dn_mfp', 'COLOR LASERJET CM2320DN MFP'),
        ('color_laserjet_cm2320_mfp', 'COLOR LASERJET CM2320 MFP'),
        ('ir_adv_4225', 'IR-ADV-4225'),
        ('designjet_t1700dr_postscript', 'DesignJet T1700dr PostScript'),
        ('designjet_t1100_44in', 'Designjet T1100 44in'),
        ('probook_45sr', 'PROBOOK 45SR'),
        ('latitude_5520', 'LATITUDE 5520'),
        ('latitude_5500', 'LATITUDE 5500'),
        ('latitude_e5500', 'LATITUDE E5500'),
        ('rpl8822be_eac', 'RPL8822BE EAC'),
        ('precision_t7400', 'PRECISION T7400'),
        ('casio_xj_f211wn', 'CASIO XJ-F211WN'),
        ('lecbio_x628', 'LECBIO - X628'),
        ('otro', 'Otro'),
    ]

    ESTADO_CHOICES = [
        ('sin_empezar', 'Sin empezar'),
        ('en_curso', 'En curso'),
        ('omitida', 'Omitida'),
        ('completada', 'Completada'),
    ]

    id_soporte = models.ForeignKey(
        User,
        related_name='soportes_realizadas',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        limit_choices_to=Q(role='soporte') | Q(role='admin'),
        verbose_name="Soporte que realizó la actividad"
    )
    id_estacion = models.ForeignKey(
        Item,
        related_name='soportes',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Estación"
    )
    actividad = models.CharField(
        max_length=100,
        choices=ACTIVIDAD_CHOICES,
        verbose_name="Actividad realizada"
    )
    lugar = models.CharField(
        max_length=50,
        choices=LUGAR_CHOICES,
        verbose_name="Lugar de trabajo"
    )
    tipo = models.CharField(
        max_length=50,
        choices=TIPO_CHOICES,
        blank=True,
        null=True,
        verbose_name="Tipo de dispositivo"
    )
    modelo = models.CharField(
        max_length=100,
        choices=MODELO_CHOICES,
        blank=True,
        null=True,
        verbose_name="Modelo de equipo"
    )
    estado = models.CharField(
        max_length=20,
        choices=ESTADO_CHOICES,
        verbose_name="Estado de la actividad"
    )
    detalle = models.TextField(
        blank=True,
        verbose_name="Detalle del trabajo"
    )
    fecha_hora_registro = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Fecha y hora de registro"
    )

    def __str__(self):
        return f"{self.id_soporte} - {self.actividad} en {self.lugar}"



 


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
    
