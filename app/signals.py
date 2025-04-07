from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.apps import apps
from django.db.models.signals import post_save
#from django.contrib.auth.models import User
from django.apps import apps

Item = apps.get_model('app', 'Item')


@receiver(post_migrate)
def create_admin_group(sender, **kwargs):
#def create_admin_group():
    if sender.name != "app":  # Reemplaza "app" con el nombre exacto de tu aplicación
        return

    try:
        Item = apps.get_model('app', 'Item')  # Obtiene modelos dinámicamente
        User = apps.get_model('auth', 'User')  # Usa 'auth' para el modelo de usuario

        admin_group, created = Group.objects.get_or_create(name='Dashboard Admin')

    # Obtener ContentType de los modelos
        item_content_type = ContentType.objects.get_for_model(Item)
        user_content_type = ContentType.objects.get_for_model(User)

    # Crear permisos si no existen
        view_item_permission, _ = Permission.objects.get_or_create(
            codename='view_item',
            name='Can view item',
            content_type=item_content_type,
        )

        view_user_permission, _ = Permission.objects.get_or_create(
            codename='view_user',
            name='Can view user',
            content_type=user_content_type,
        )

    # Asignar permisos al grupo
        admin_group.permissions.add(view_item_permission, view_user_permission)

    except Exception as e:
        print(f"Error en la creación de permisos o grupo: {e}")
