#from .views import  custom_login, cambiar_estado, solicitar_soporte, custom_logout,  actualizar_estado_tarea
#from .views import views, UserViewSet, ItemViewSet, ComplementoViewSet, dashboard,  dashboard_soporte, dashboard_operador, dashboard_admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    custom_login, cambiar_estado, solicitar_soporte, custom_logout, actualizar_estado_tarea,
    UserViewSet, ItemViewSet, ComplementoViewSet, dashboard, dashboard_soporte, dashboard_operador, dashboard_admin
)
#from app.views import custom_logout



# Configuración del enrutador para las vistas de API
router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'items', ItemViewSet, basename='item')
router.register(r'complementos', ComplementoViewSet)

urlpatterns = [
    path('', include(router.urls)),  # Incluye todas las rutas de la API
    path('api/', include(router.urls)),
    #path('api/', include('app.urls')),

    path('dashboard/', dashboard, name='dashboard'),
    path('dashboard/operador/', dashboard_operador, name='dashboard_operador'),
    path('dashboard/soporte/', dashboard_soporte, name='dashboard_soporte'),
    path('dashboard/admin/', dashboard_admin, name='dashboard_admin'),

    path('login/', custom_login, name='login'),
    path('logout/', custom_logout, name='logout'),

    #path('cambiar_estado/<int:item_id>/<str:nuevo_estado>/', cambiar_estado, name='cambiar_estado'),
    path('actualizar_estado/', actualizar_estado_tarea, name='actualizar_estado'),
    path('solicitar_soporte/<int:item_id>/', solicitar_soporte, name='solicitar_soporte'),

    #path('actualizar-tarea/', actualizar_estado_tarea, name='actualizar_estado_tarea'),
    path('api/actualizar_estado/', actualizar_estado_tarea, name='actualizar_estado_tarea'),
    

]

# Agregar las rutas generadas por el enrutador
urlpatterns += router.urls
