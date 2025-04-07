from rest_framework import serializers
from django.contrib.auth import get_user_model
#from django.contrib.auth.models import User
from .models import Item, Complemento

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
   # role = serializers.CharField(source='get_role_display', read_only=True)

    #class Meta:
    #    model = get_user_model()
    #    fields = ['id', 'username', 'email', 'role']
    
     class Meta:
        model = User
        #fields = ['id', 'username', 'email', 'role', 'is_active']  # Se incluye 'is_active'
        fields = ['id', 'username', 'email', 'role', 'is_active', 'date_of_birth', 'phone_number', 'address', 'permissions']

class ItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = Item
        #fields = '__all__'
        #fields = ['id', 'nombre', 'descripcion', 'estado', 'asignado_a', 'seguimiento_por', 'fecha_creacion', 'codigo_qr']
        fields = ['id', 'nombre', 'cont_R', 'cont_C', 'estado', 'asignado_a', 'seguimiento_por', 'fecha_creacion', 'codigo_qr']
        read_only_fields = ['ticket_id', 'qr_code']  # No se deben modificar manualmente
        
class ComplementoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Complemento
        fields = '__all__'

#class ItemSerializer(serializers.ModelSerializer):
#   complementos = ComplementoSerializer(many=True, read_only=True)

#    class Meta:
#        model = Item
#        fields = ['id', 'nombre', 'descripcion', 'precio', 'complementos']
class ItemComplementoSerializer(serializers.ModelSerializer):
    complementos = ComplementoSerializer(many=True, read_only=True)

    class Meta:
        model = Item
        fields = ['id', 'nombre', 'descripcion', 'precio', 'complementos']
