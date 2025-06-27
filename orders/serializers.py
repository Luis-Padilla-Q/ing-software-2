from rest_framework import serializers
from django.contrib.auth.models import User
from .models import *

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']

class PerfilSerializer(serializers.ModelSerializer):
    usuario = UserSerializer()

    class Meta:
        model = Perfil
        fields = ['id', 'usuario', 'rol', 'telefono', 'direccion', 'fecha_registro']

class CategoriaProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoriaProducto
        fields = '__all__'

class LocalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Local
        fields = '__all__'

class ProductoSerializer(serializers.ModelSerializer):
    es_favorito = serializers.SerializerMethodField()

    class Meta:
        model = Producto
        fields = ['id', 'local', 'categoria', 'nombre', 'precio', 'disponibilidad', 'es_favorito']

    def get_es_favorito(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated and hasattr(request.user, 'perfil'):
            return obj in request.user.perfil.favoritos.all()
        return False

class RepartidorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Repartidor
        fields = '__all__'

class PedidoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pedido
        fields = '__all__'

class DetallePedidoSerializer(serializers.ModelSerializer):
    class Meta:
        model = DetallePedido
        fields = '__all__'

class PagoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pago
        fields = '__all__'

class EntregaPedidoSerializer(serializers.ModelSerializer):
    class Meta:
        model = EntregaPedido
        fields = '__all__'

class CalificacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Calificacion
        fields = '__all__'
