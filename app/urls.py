#from .views import  custom_login, cambiar_estado, solicitar_soporte, custom_logout,  actualizar_estado_tarea
#from .views import views, UserViewSet, ItemViewSet, ComplementoViewSet, dashboard,  dashboard_soporte, dashboard_operador, dashboard_admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    custom_login, cambiar_estado, solicitar_soporte, custom_logout, actualizar_estado_tarea,
    UserViewSet, ItemViewSet, ComplementoViewSet, dashboard, dashboard_soporte, dashboard_operador, dashboard_admin
)
#from app.views import custom_logout
from django.urls import path
from . import views
from app import views


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
    #path('dashboard/admin/', dashboard_admin, name='dashboard_admin'),
    path('dashboard/admin/', views.lista_items, name='dashboard_admin'),

    path('login/', custom_login, name='login'),
    path('logout/', custom_logout, name='logout'),

    #path('cambiar_estado/<int:item_id>/<str:nuevo_estado>/', cambiar_estado, name='cambiar_estado'),
    path('actualizar_estado/', actualizar_estado_tarea, name='actualizar_estado'),
    path('solicitar_soporte/<int:item_id>/', solicitar_soporte, name='solicitar_soporte'),

    #path('actualizar-tarea/', actualizar_estado_tarea, name='actualizar_estado_tarea'),
    path('api/actualizar_estado/', actualizar_estado_tarea, name='actualizar_estado_tarea'),
    

    #path('view/items/', views.lista_items, name='lista_items'),
    #path('generar-pdf/', views.generar_pdf_items_qr, name='generar_pdf'),
    path('generar-pdf-item/<int:item_id>/', views.generar_pdf_item_qr, name='generar_pdf_item'),
    path('view/items/<int:item_id>/', views.item_detail_html, name='item_detail_html'),
    # generar todos los qrs
    path('generartodosqrs/', views.generar_todos_qrs, name='generar_todos_qrs'),

    #bienvenida soporte
    path('soporte/bienvenida/', views.bienvenida_soporte, name='bienvenidaSoporte'),
    #vista trasmision
    path('soporte/transmision/', views.transmision_soporte, name='transmisionSoporte'),
    #vista reportes
    path('soporte/reporte/', views.reporte_soporte, name='reporteSoporte'),
]
