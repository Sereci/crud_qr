from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model
from django import forms
from django.utils.html import mark_safe
#from .models import User, Item
from .models import Item

User = get_user_model()

class UserAdminForm(forms.ModelForm):
    class Meta:
        model = User
        fields = '__all__'

    def clean_role(self):
        """Valida que el rol ingresado sea válido"""
        role = self.cleaned_data.get('role')
        if role not in ['admin', 'soporte', 'operador']:
            raise forms.ValidationError("Rol inválido")
        return role

    def clean_password(self):
        """Asegura que la contraseña ingresada en el formulario no esté en texto plano"""
        password = self.cleaned_data.get("password")
        if not password:  # Si el campo está vacío, mantiene la contraseña actual
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
        """Mantiene la contraseña anterior si no se proporciona una nueva"""
        if change and 'password' in form.cleaned_data:
            password = form.cleaned_data.get("password")
            if password and not password.startswith('pbkdf2_sha256$'):
                obj.set_password(password)  # Encripta la nueva contraseña
            else:
                obj.password = User.objects.get(pk=obj.pk).password  # Mantiene la contraseña anterior
        
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