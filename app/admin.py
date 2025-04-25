from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model
from django import forms
from django.utils.html import mark_safe
from .models import Item, Oficina, HistoricoMovimiento, Activo
import openpyxl
from django.http import HttpResponse
from django.utils.html import format_html
from django.urls import path
from django.shortcuts import render, get_object_or_404
from .models import Oficina, HistoricoMovimiento, Item


class OficinaAdmin(admin.ModelAdmin):
    list_display = ('nombre_de_la_oficina', 'ubicacion')
    change_list_template = "admin/oficinas_changelist.html"

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                'rutas/<int:oficina_id>/',
                self.admin_site.admin_view(self.ver_rutas),
                name='ver_rutas',
            ),
        ]
        return custom_urls + urls

    def ver_rutas(self, request, oficina_id):
        oficina = get_object_or_404(Oficina, pk=oficina_id)
        historicos = HistoricoMovimiento.objects.filter(oficina=oficina).select_related('item')
        
        context = {
            'oficina': oficina,
            'historicos': historicos,
            'title': f'Rutas de {oficina.nombre_de_la_oficina}',
        }
        return render(request, 'admin/ver_rutas.html', context)


#admin.site.register(Oficina, OficinaAdmin)



User = get_user_model()
def export_as_excel(modeladmin, request, queryset):
    from openpyxl import Workbook
    from django.http import HttpResponse
    import datetime

    wb = Workbook()
    ws = wb.active
    ws.title = "Datos Exportados"

    # Campos específicos a exportar
    export_fields = [
        'nombre',
        'ticket_id',
        'cont_C',
        'cont_R',
        'soporte',
        'asignado_a',
        'seguimiento_por'
    ]

    # Agregar encabezados con contador
    ws.append(['N°'] + export_fields)

    # Escribir datos
    for idx, obj in enumerate(queryset, start=1):
        row = [idx]  # Contador

        for field in export_fields:
            value = getattr(obj, field)

            # Quitar zona horaria si es datetime
            if isinstance(value, datetime.datetime) and value.tzinfo is not None:
                value = value.replace(tzinfo=None)

            if value is None:
                value = ""
            elif hasattr(value, '__str__'):
                value = str(value)

            row.append(value)

        ws.append(row)

    # Preparar respuesta
    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    )
    response['Content-Disposition'] = 'attachment; filename=exportado.xlsx'
    wb.save(response)
    return response

export_as_excel.short_description = "Exportar seleccionados a Excel"



class UserAdminForm(forms.ModelForm):
    class Meta:
        model = User
        fields = '__all__'

    def clean_role(self):
        """Valida que el rol ingresado sea válido"""
        role = self.cleaned_data.get('role')
        if role not in ['admin', 'soporte', 'operador','coordi']:
            raise forms.ValidationError("Rol inválido")
        return role

    def clean_password(self):
        """Asegura que la contraseña ingresada en el formulario no esté en texto plano"""
        password = self.cleaned_data.get("password")
        if not password:
            return self.instance.password
        return password

class CustomUserAdmin(UserAdmin):
    form = UserAdminForm
    list_display = ('username', 'email', 'role', 'date_of_birth', 'phone_number', 'is_active', 'is_staff')
    list_filter = ('role', 'is_active', 'is_staff')
    fieldsets = UserAdmin.fieldsets + (
        ('Información Personal', {'fields': ('date_of_birth', 'phone_number', 'address')}),
        ('Permisos Personalizados', {'fields': ('permissions',)}),
        ('Información Adicional', {'fields': ('role',)}),
    )

    def save_model(self, request, obj, form, change):
        if change and 'password' in form.cleaned_data:
            password = form.cleaned_data.get("password")
            if password and not password.startswith('pbkdf2_sha256$'):
                obj.set_password(password)
            else:
                obj.password = User.objects.get(pk=obj.pk).password
        obj.save()


admin.site.register(User, CustomUserAdmin)


class ItemAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'ticket_id', 'cont_R', 'cont_C', 'estado', 'asignado_a', 'seguimiento_por', 'fecha_creacion')
    readonly_fields = ('ticket_id', 'cont_R', 'cont_C','nombre') 
    list_filter = ('estado', 'asignado_a', 'seguimiento_por')
    search_fields = ('nombre','ticket_id')
    actions = [export_as_excel]
       

    def mostrar_qr(self, obj):
        if obj.codigo_qr:
            return mark_safe(f'<img src="{obj.codigo_qr.url}" width="100" height="100" />')
        return "No disponible"

    mostrar_qr.short_description = "Código QR"    

admin.site.register(Item, ItemAdmin)


# Nuevos modelos
@admin.register(Oficina)
class OficinaAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'nombre_de_la_oficina', 'ubicacion', 'georefenciacido')
    search_fields = ('codigo', 'nombre_de_la_oficina')
    change_list_template = "admin/oficinas_changelist.html"

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                'rutas/<int:oficina_id>/',
                self.admin_site.admin_view(self.ver_rutas),
                name='ver_rutas',
            ),
        ]
        return custom_urls + urls

    def ver_rutas(self, request, oficina_id):
        oficina = get_object_or_404(Oficina, pk=oficina_id)
        historicos = HistoricoMovimiento.objects.filter(oficina=oficina).select_related('item')
        context = {
            'oficina': oficina,
            'historicos': historicos,
            'title': f'Rutas de {oficina.nombre_de_la_oficina}',
        }
        return render(request, 'admin/ver_rutas.html', context)



@admin.register(HistoricoMovimiento)
class HistoricoMovimientosAdmin(admin.ModelAdmin):
    list_display = ('fecha_de_llegada', 'responsable','oficina')
    search_fields = ('responsable__username', 'item__ticket_id')  # Asegúrate de que Item tenga 'nombre'


@admin.register(Activo)
class ActivosAdmin(admin.ModelAdmin):
    list_display = ('tipo_de_equipo', 'item','maleta', 'laptop_y_cargador', 'monitor_cable_vga_y_poder', 'teclado_mouse', 'impresora')
    list_filter = ('tipo_de_equipo', 'banner', 'tripode', 'cable_de_extension')
