from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model
from django import forms
from django.utils.html import mark_safe
from .models import Item, Oficina, HistoricoMovimiento, Activo

User = get_user_model()


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
    list_filter = ('estado', 'asignado_a', 'seguimiento_por')
    search_fields = ('nombre',)

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


@admin.register(HistoricoMovimiento)
class HistoricoMovimientosAdmin(admin.ModelAdmin):
    list_display = ('fecha_de_llegada', 'responsable','oficina')
    search_fields = ('responsable__username', 'item__ticket_id')  # Asegúrate de que Item tenga 'nombre'


@admin.register(Activo)
class ActivosAdmin(admin.ModelAdmin):
    list_display = ('tipo_de_equipo', 'item','maleta', 'laptop_y_cargador', 'monitor_cable_vga_y_poder', 'teclado_mouse', 'impresora')
    list_filter = ('tipo_de_equipo', 'banner', 'tripode', 'cable_de_extension')
