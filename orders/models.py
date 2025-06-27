from django.db import models
from django.contrib.auth.models import User

class Local(models.Model):
    nombre = models.CharField(max_length=100)
    direccion = models.TextField()
    telefono = models.CharField(max_length=15)
    email = models.EmailField()
    estado = models.CharField(max_length=50)
    calificacion = models.FloatField(default=0)

    def __str__(self):
        return self.nombre

class CategoriaProducto(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()

    def __str__(self):
        return self.nombre

class Producto(models.Model):
    local = models.ForeignKey(Local, on_delete=models.CASCADE)
    categoria = models.ForeignKey(CategoriaProducto, on_delete=models.SET_NULL, null=True)
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    precio = models.DecimalField(max_digits=6, decimal_places=2)
    imagen = models.ImageField(upload_to='productos/', null=True, blank=True)
    disponibilidad = models.IntegerField(default=0)

    def __str__(self):
        return self.nombre

class Pedido(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    productos = models.ManyToManyField(Producto)
    fecha = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=8, decimal_places=2)
    estado = models.CharField(max_length=50, choices=[
        ('pendiente', 'Pendiente'),
        ('enviado', 'Enviado'),
        ('entregado', 'Entregado')
    ])

    def __str__(self):
        return f'Pedido {self.id} - {self.estado}'
    
class Perfil(models.Model):
    ROLES = [
        ('cliente', 'Cliente'),
        ('empleado', 'Empleado'),
        ('repartidor', 'Repartidor'),
        ('admin_local', 'Administrador de Local'),
    ]
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    rol = models.CharField(max_length=20, choices=ROLES)
    telefono = models.CharField(max_length=15)
    direccion = models.TextField(blank=True)
    fecha_registro = models.DateField(auto_now_add=True)
    favoritos = models.ManyToManyField('Producto', blank=True, related_name='favoritos_por')  # ✅ nuevo

    def __str__(self):
        return f"{self.usuario.username} ({self.rol})"

class Repartidor(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    telefono = models.CharField(max_length=15)
    email = models.EmailField()
    disponibilidad = models.BooleanField(default=True)
    local = models.ForeignKey(Local, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"

class Pedido(models.Model):
    cliente = models.ForeignKey(User, on_delete=models.CASCADE)
    local = models.ForeignKey(Local, on_delete=models.CASCADE)
    repartidor = models.ForeignKey(Repartidor, on_delete=models.SET_NULL, null=True, blank=True)
    fecha_hora = models.DateTimeField(auto_now_add=True)
    estado_pedido = models.CharField(max_length=50)
    monto = models.FloatField()
    direccion_entrega = models.TextField()

    def __str__(self):
        return f"Pedido {self.id} - Cliente: {self.cliente.username}"

class DetallePedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    fecha_hora = models.DateTimeField(auto_now_add=True)
    precio_unitario = models.FloatField()

    def __str__(self):
        return f"Detalle {self.id} - Pedido {self.pedido.id}"

class Pago(models.Model):
    pedido = models.OneToOneField(Pedido, on_delete=models.CASCADE)
    metodo_pago = models.CharField(max_length=50)
    monto = models.FloatField()
    fecha_pago = models.DateTimeField(auto_now_add=True)
    estado_pago = models.CharField(max_length=50)

    def __str__(self):
        return f"Pago Pedido {self.pedido.id}"

class EntregaPedido(models.Model):
    pedido = models.OneToOneField(Pedido, on_delete=models.CASCADE)
    cliente = models.ForeignKey(User, on_delete=models.CASCADE)
    repartidor = models.ForeignKey(Repartidor, on_delete=models.CASCADE)
    estado_entrega = models.CharField(max_length=50)
    hora_inicio = models.TimeField()
    hora_entrega = models.TimeField(null=True, blank=True)

    def __str__(self):
        return f"Entrega {self.id} - Pedido {self.pedido.id}"

class Calificacion(models.Model):
    entrega = models.ForeignKey(EntregaPedido, on_delete=models.CASCADE)
    cliente = models.ForeignKey(User, on_delete=models.CASCADE)
    calificacion = models.FloatField()
    comentario = models.TextField(blank=True)
    fecha = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Calificación {self.id} - Cliente {self.cliente.username}"

