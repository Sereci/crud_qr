from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model
from django import forms
from django.utils.html import mark_safe
from django.utils import timezone
from .models import Item, Oficina, HistoricoMovimiento, Activo
import openpyxl
from django.http import HttpResponse
from django.urls import path
from django.shortcuts import render, get_object_or_404

User = get_user_model()


# -------------------- EXPORTACIÓN --------------------
def export_as_excel(modeladmin, request, queryset):
    from openpyxl import Workbook
    import datetime

    wb = Workbook()
    ws = wb.active
    ws.title = "Datos Exportados"
    export_fields = [
        'nombre', 'ticket_id', 'cont_C', 'cont_R',
        'soporte', 'asignado_a', 'seguimiento_por'
    ]
    ws.append(['N°'] + export_fields)
    for idx, obj in enumerate(queryset, start=1):
        row = [idx]
        for field in export_fields:
            value = getattr(obj, field)
            if isinstance(value, datetime.datetime) and value.tzinfo is not None:
                value = value.replace(tzinfo=None)
            row.append(str(value) if value is not None else "")
        ws.append(row)
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=exportado.xlsx'
    wb.save(response)
    return response

export_as_excel.short_description = "Exportar seleccionados a Excel"


# -------------------- USER --------------------
class UserAdminForm(forms.ModelForm):
    class Meta:
        model = User
        fields = '__all__'

    def clean_role(self):
        role = self.cleaned_data.get('role')
        if role not in ['admin', 'soporte', 'operador', 'coordi', 'logistica']:
            raise forms.ValidationError("Rol inválido")
        return role

    def clean_password(self):
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


# -------------------- ITEM --------------------
class ItemAdminForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

    def clean_description(self):
        nueva = self.cleaned_data.get("description", "")
        original = self.instance.description or ""
        var1 = original
        var3 = original[:len(original)]

        original = self.instance.description or ""

        # Normalizamos saltos de línea (\r\n -> \n)
        nueva = nueva.replace('\r\n', '\n')
        original = original.replace('\r\n', '\n')

        # Convertimos a listas
        vector_original = list(original)
        vector_nueva = list(nueva)
        sw = False
        print('*************************************')
        print("Original:", vector_original)
        print("Nueva   :", vector_nueva)
        print("Longitudes:", len(vector_original), len(vector_nueva))

        min_len = min(len(vector_original), len(vector_nueva))

        # Comparamos hasta la longitud del original
        if vector_original == vector_nueva[:len(vector_original)]:
            print('✅ Son iguales (o nueva es una extensión del original)')
            sw= True
        else:
            print('❌ No son iguales')
            diferencias = []
            for i in range(min_len):
                if vector_original[i] != vector_nueva[i]:
                    diferencias.append(f" - Posición {i}: '{vector_original[i]}' != '{vector_nueva[i]}'")
            
            if diferencias:
                print("Diferencias en posiciones:")
                for diferencia in diferencias:
                    print(diferencia)
                    sw=False
            else:
                print("No hay diferencias (pero las longitudes son diferentes)")
                sw=True

        if sw!=True:
            raise forms.ValidationError("No se puede borrar ni modificar el texto ya registrado. Volver a Seleccional el Item y Modificar")

        # Si se agregó algo nuevo, anexar firma
        if var3 >= var1:
            username = self.user.username if self.user else "desconocido"
            timestamp = timezone.now().strftime("%d/%m/%Y %H:%M:%S")
            firma = f"\n{timestamp} {username}\n" + "-" * 46 + "\n"
            nueva = nueva + firma

        return nueva

class ItemAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'ticket_id', 'cont_R', 'cont_C', 'estado', 'asignado_a', 'seguimiento_por', 'fecha_creacion')
    list_filter = ('estado', 'asignado_a', 'seguimiento_por')
    search_fields = ('nombre', 'ticket_id')
    actions = [export_as_excel]
    form = ItemAdminForm

    def get_form(self, request, obj=None, **kwargs):
        kwargs['form'] = self.form
        form_class = super().get_form(request, obj, **kwargs)
        class WrappedForm(form_class):
            def __init__(self2, *args, **kwargs2):
                kwargs2['user'] = request.user
                super().__init__(*args, **kwargs2)
        return WrappedForm

    def get_readonly_fields(self, request, obj=None):
        if request.user.role in ('soporte', 'logistica','operador','coordi'):
            return ('ticket_id', 'cont_R', 'cont_C', 'estado', 'asignado_a', 'seguimiento_por', 'nombre','soporte','codigo_qr')
        return super().get_readonly_fields(request, obj)

    def mostrar_qr(self, obj):
        if obj.codigo_qr:
            return mark_safe(f'<img src="{obj.codigo_qr.url}" width="100" height="100" />')
        return "No disponible"

    mostrar_qr.short_description = "Código QR"

admin.site.register(Item, ItemAdmin)


# -------------------- OFICINA --------------------
@admin.register(Oficina)
class OficinaAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'nombre_de_la_oficina', 'ubicacion', 'georefenciacido')
    search_fields = ('codigo', 'nombre_de_la_oficina')
    change_list_template = "admin/oficinas_changelist.html"

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('rutas/<int:oficina_id>/', self.admin_site.admin_view(self.ver_rutas), name='ver_rutas'),
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


# -------------------- HISTÓRICO --------------------
@admin.register(HistoricoMovimiento)
class HistoricoMovimientosAdmin(admin.ModelAdmin):
    list_display = ('fecha_de_llegada', 'responsable', 'oficina')
    search_fields = ('responsable__username', 'item__ticket_id')


# -------------------- ACTIVO --------------------
@admin.register(Activo)
class ActivosAdmin(admin.ModelAdmin):
    list_display = ('tipo_de_equipo', 'item', 'maleta', 'laptop_y_cargador', 'monitor_cable_vga_y_poder', 'teclado_mouse', 'impresora')
    list_filter = ('tipo_de_equipo', 'banner', 'tripode', 'cable_de_extension')
