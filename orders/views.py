from rest_framework import viewsets
from rest_framework import filters
from .models import *
from .serializers import *
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from .permissions import IsCliente, IsAdminLocal
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .permissions import IsAdminLocal 
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework import status

class PerfilViewSet(viewsets.ModelViewSet):
    queryset = Perfil.objects.all()
    serializer_class = PerfilSerializer

    @action(detail=False, methods=['post'], url_path='toggle-favorito')
    def toggle_favorito(self, request):
        user = request.user
        if not hasattr(user, 'perfil'):
            return Response({"error": "No tiene perfil"}, status=400)

        producto_id = request.data.get('producto_id')
        try:
            producto = Producto.objects.get(id=producto_id)
        except Producto.DoesNotExist:
            return Response({"error": "Producto no existe"}, status=404)

        perfil = user.perfil
        if producto in perfil.favoritos.all():
            perfil.favoritos.remove(producto)
            return Response({"mensaje": "Eliminado de favoritos"})
        else:
            perfil.favoritos.add(producto)
            return Response({"mensaje": "Agregado a favoritos"})

class LocalViewSet(viewsets.ModelViewSet):
    queryset = Local.objects.all()
    serializer_class = LocalSerializer

class CategoriaProductoViewSet(viewsets.ModelViewSet):
    queryset = CategoriaProducto.objects.all()
    serializer_class = CategoriaProductoSerializer

class ProductoViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['nombre']  # barra de búsqueda
    filterset_fields = ['categoria__nombre', 'local']

    def get_serializer_context(self):
        return {'request': self.request}
    
    def get_queryset(self):
        queryset = Producto.objects.all()
        user = self.request.user

        categoria = self.request.query_params.get('categoria')
        if categoria:
            queryset = queryset.filter(categoria__nombre__iexact=categoria)

        if self.request.query_params.get('favoritos') == 'true':
            if user.is_authenticated and hasattr(user, 'perfil'):
                return user.perfil.favoritos.all()
            else:
                return Producto.objects.none()

        return queryset

class RepartidorViewSet(viewsets.ModelViewSet):
    queryset = Repartidor.objects.all()
    serializer_class = RepartidorSerializer

class PedidoViewSet(viewsets.ModelViewSet):
    queryset = Pedido.objects.all()
    serializer_class = PedidoSerializer

class DetallePedidoViewSet(viewsets.ModelViewSet):
    queryset = DetallePedido.objects.all()
    serializer_class = DetallePedidoSerializer

class PagoViewSet(viewsets.ModelViewSet):
    queryset = Pago.objects.all()
    serializer_class = PagoSerializer

class EntregaPedidoViewSet(viewsets.ModelViewSet):
    queryset = EntregaPedido.objects.all()
    serializer_class = EntregaPedidoSerializer

class CalificacionViewSet(viewsets.ModelViewSet):
    queryset = Calificacion.objects.all()
    serializer_class = CalificacionSerializer

class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        token = Token.objects.get(key=response.data['token'])
        perfil = Perfil.objects.get(usuario=token.user)
        return Response({
            'token': token.key,
            'user_id': token.user_id,
            'username': token.user.username,
            'rol': perfil.rol
        })
class PedidoViewSet(viewsets.ModelViewSet):
    queryset = Pedido.objects.all()
    serializer_class = PedidoSerializer
    permission_classes = [IsAuthenticated, IsCliente]  # Solo clientes

    def get_queryset(self):
        # Solo ver pedidos del cliente autenticado
        user = self.request.user
        return Pedido.objects.filter(cliente=user)
class LocalViewSet(viewsets.ModelViewSet):
    queryset = Local.objects.all()
    serializer_class = LocalSerializer
    permission_classes = [IsAuthenticated, IsAdminLocal]
