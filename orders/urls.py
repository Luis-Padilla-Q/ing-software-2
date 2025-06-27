from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r'perfiles', PerfilViewSet)
router.register(r'locales', LocalViewSet)
router.register(r'categorias', CategoriaProductoViewSet)
router.register(r'productos', ProductoViewSet)
router.register(r'repartidores', RepartidorViewSet)
router.register(r'pedidos', PedidoViewSet)
router.register(r'detalles', DetallePedidoViewSet)
router.register(r'pagos', PagoViewSet)
router.register(r'entregas', EntregaPedidoViewSet)
router.register(r'calificaciones', CalificacionViewSet)

urlpatterns = [
    path('', include(router.urls)),
]

urlpatterns += [
    path('login/', CustomAuthToken.as_view(), name='api_login'),
]