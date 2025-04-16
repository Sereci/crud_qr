from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from app import views

urlpatterns = [
    # Acceso al panel de administración
    path('admin/', admin.site.urls),

    # Rutas de login/logout
    path('login/', views.custom_login, name='login'),
    path('logout/', views.custom_logout, name='logout'),

    # Ruta para el dashboard principal
    path('dashboard/', views.dashboard, name='dashboard'),

    # Rutas de la API (solo una vez)
    path('api/', include('app.urls')),  #

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
