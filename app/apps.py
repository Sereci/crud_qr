from django.apps import AppConfig
from django.core.exceptions import AppRegistryNotReady
#from django.contrib.auth.models import Group, Permission
#from django.contrib.contenttypes.models import ContentType
from django.db.utils import OperationalError, ProgrammingError
import django




class AppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app'  # Asegúrate de que el nombre sea el correcto

#    def ready(self):
#        print("La aplicación 'app' está completamente cargada")  # Esto debe imprimirse en la consola
#        try:
#            #import app.signals  # Intentamos importar las señales
#            import app.signals
#        except ImportError as e:
#            print(f"Error al importar señales: {e}")