# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#     * Rearrange models' order
#     * Make sure each model has one field with primary_key=True
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [appname]'
# into your database.
from __future__ import unicode_literals

from django.db import models

class AsignacionSupervisorPlaza(models.Model):
    id = models.IntegerField(primary_key=True)
    usuario = models.ForeignKey('Usuario', db_column='usuario')
    sucursal = models.ForeignKey('Sucursal', db_column='sucursal')
    class Meta:
        db_table = 'asignacion_supervisor_plaza'

class Cambio(models.Model):
    id = models.IntegerField()
    sucursal = models.IntegerField()
    folio_ticket = models.CharField(max_length=145L)
    fecha = models.DateTimeField()
    modelo_entrada = models.CharField(max_length=45L)
    modelo_salida = models.CharField(max_length=45L)
    diferencia_precio = models.FloatField()
    motivo_cambio = models.TextField()
    class Meta:
        db_table = 'cambio'

class CategoriaProducto(models.Model):
    id = models.IntegerField(primary_key=True)
    categoria = models.CharField(max_length=45L, db_column='Categoria') # Field name made lowercase.
    class Meta:
        db_table = 'categoria_producto'

class ClienteDatos(models.Model):
    id = models.IntegerField()
    nombre = models.CharField(max_length=100L)
    telefono = models.CharField(max_length=100L, db_column='Telefono') # Field name made lowercase.
    correo = models.CharField(max_length=100L)
    pais = models.CharField(max_length=50L)
    estado = models.CharField(max_length=50L)
    municipio = models.CharField(max_length=45L)
    sucursal = models.ForeignKey('Sucursal', db_column='sucursal')
    descuentos = models.CharField(max_length=45L)
    fecha = models.DateTimeField(null=True, blank=True)
    usuario_creador = models.IntegerField()
    class Meta:
        db_table = 'cliente_datos'

class ClienteFacturacion(models.Model):
    id = models.IntegerField(primary_key=True)
    rfc = models.CharField(max_length=150L)
    calle = models.CharField(max_length=150L)
    colonia = models.CharField(max_length=150L)
    num_int = models.CharField(max_length=45L)
    num_ext = models.CharField(max_length=45L)
    cod_postal = models.CharField(max_length=45L)
    cliente_datos = models.ForeignKey(ClienteDatos, db_column='cliente_datos')
    class Meta:
        db_table = 'cliente_facturacion'

class DjangoContentType(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100L)
    app_label = models.CharField(max_length=100L)
    model = models.CharField(max_length=100L)
    class Meta:
        db_table = 'django_content_type'

class DjangoSession(models.Model):
    session_key = models.CharField(max_length=40L, primary_key=True)
    session_data = models.TextField()
    expire_date = models.DateTimeField()
    class Meta:
        db_table = 'django_session'

class DjangoSite(models.Model):
    id = models.IntegerField(primary_key=True)
    domain = models.CharField(max_length=100L)
    name = models.CharField(max_length=50L)
    class Meta:
        db_table = 'django_site'

class Estados(models.Model):
    id_estado = models.IntegerField()
    estado = models.CharField(max_length=60L)
    class Meta:
        db_table = 'estados'

class Eventos(models.Model):
    id = models.IntegerField(primary_key=True)
    nombre_evento = models.CharField(max_length=45L)
    class Meta:
        db_table = 'eventos'

class Inventario(models.Model):
    id = models.IntegerField(primary_key=True)
    producto = models.ForeignKey('Producto', db_column='Producto_id') # Field name made lowercase.
    sucursal = models.ForeignKey('Sucursal', db_column='Sucursal_id') # Field name made lowercase.
    existencia = models.IntegerField(null=True, blank=True)
    stock = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = 'inventario'

class Log(models.Model):
    id = models.IntegerField(primary_key=True)
    date = models.DateTimeField(null=True, blank=True)
    usuario = models.ForeignKey('Usuario')
    eventos = models.ForeignKey(Eventos)
    class Meta:
        db_table = 'log'

class Municipios(models.Model):
    id_municipio = models.IntegerField(null=True, blank=True)
    id_pk_estado = models.IntegerField(null=True, db_column='id_PK_estado', blank=True) # Field name made lowercase.
    municipio = models.CharField(max_length=49L, blank=True)
    class Meta:
        db_table = 'municipios'

class Producto(models.Model):
    id = models.IntegerField(primary_key=True)
    categoria_producto = models.ForeignKey(CategoriaProducto, db_column='categoria_producto')
    codigo = models.CharField(max_length=45L)
    descripcion = models.CharField(max_length=45L)
    class Meta:
        db_table = 'producto'

class ProductoHasRango(models.Model):
    id = models.IntegerField(primary_key=True)
    producto = models.ForeignKey(Producto, db_column='Producto_id') # Field name made lowercase.
    rango = models.ForeignKey('Rango', db_column='rango')
    sucursal = models.ForeignKey('Sucursal', db_column='Sucursal_id') # Field name made lowercase.
    costo = models.FloatField(null=True, blank=True)
    class Meta:
        db_table = 'producto_has_rango'

class Rango(models.Model):
    id = models.IntegerField(primary_key=True)
    min = models.IntegerField(null=True, db_column='Min', blank=True) # Field name made lowercase.
    max = models.IntegerField(null=True, db_column='Max', blank=True) # Field name made lowercase.
    class Meta:
        db_table = 'rango'

class Sucursal(models.Model):
    id = models.IntegerField(primary_key=True)
    nombre = models.CharField(max_length=150L)
    estado = models.CharField(max_length=100L)
    pais = models.CharField(max_length=50L)
    tel = models.CharField(max_length=50L)
    almacen_admipaq = models.CharField(max_length=100L)
    iva = models.CharField(max_length=50L)
    direccion = models.CharField(max_length=100L)
    num_int = models.CharField(max_length=50L)
    num_ext = models.CharField(max_length=45L)
    folio_sucursal = models.CharField(max_length=50L)
    descuento = models.CharField(max_length=10L)
    class Meta:
        db_table = 'sucursal'

class TastypieApiaccess(models.Model):
    id = models.IntegerField(primary_key=True)
    identifier = models.CharField(max_length=255L)
    url = models.CharField(max_length=255L)
    request_method = models.CharField(max_length=10L)
    accessed = models.IntegerField()
    class Meta:
        db_table = 'tastypie_apiaccess'

class Usuario(models.Model):
    id = models.IntegerField(primary_key=True)
    nombre = models.CharField(max_length=500L)
    rol = models.CharField(max_length=150L)
    email = models.CharField(max_length=100L)
    password = models.CharField(max_length=300L)
    tel_cel = models.CharField(max_length=100L)
    class Meta:
        db_table = 'usuario'

class UsuarioHasSucursal(models.Model):
    id = models.IntegerField(primary_key=True)
    usuario = models.ForeignKey(Usuario)
    sucursal = models.ForeignKey(Sucursal, db_column='Sucursal_id') # Field name made lowercase.
    class Meta:
        db_table = 'usuario_has_sucursal'

class UsuarioSucursal(models.Model):
    id = models.IntegerField(primary_key=True)
    tel_residencia = models.CharField(max_length=85L)
    bono = models.CharField(max_length=45L)
    porciento_comision = models.CharField(max_length=45L)
    salario_real = models.CharField(max_length=45L)
    num_seguro_social = models.CharField(max_length=100L)
    direccion = models.CharField(max_length=200L)
    nombre_aval = models.CharField(max_length=200L)
    tel_aval = models.CharField(max_length=100L)
    usuario = models.ForeignKey(Usuario)
    class Meta:
        db_table = 'usuario_sucursal'

class UsuarioSucursalHasSucursal(models.Model):
    id = models.IntegerField(primary_key=True)
    usuario_sucursal = models.ForeignKey(UsuarioSucursal)
    sucursal = models.ForeignKey(Sucursal, db_column='Sucursal_id') # Field name made lowercase.
    class Meta:
        db_table = 'usuario_sucursal_has_sucursal'

class Venta(models.Model):
    id = models.IntegerField(primary_key=True)
    sucursal = models.ForeignKey(Sucursal, db_column='Sucursal_id') # Field name made lowercase.
    fecha = models.DateTimeField()
    folio = models.IntegerField()
    total = models.FloatField()
    total_productos = models.IntegerField()
    url_reporte = models.CharField(max_length=500L)
    class Meta:
        db_table = 'venta'

class VentaCliente(models.Model):
    id = models.IntegerField(primary_key=True)
    cliente_datos = models.ForeignKey(ClienteDatos, db_column='cliente_datos')
    venta = models.ForeignKey(Venta, db_column='venta')
    class Meta:
        db_table = 'venta_cliente'

class VentaHasProducto(models.Model):
    id = models.IntegerField(primary_key=True)
    venta = models.ForeignKey(Venta, db_column='Venta_id') # Field name made lowercase.
    producto = models.ForeignKey(Producto, db_column='Producto_id') # Field name made lowercase.
    cantidad = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = 'venta_has_producto'

class VentaPublico(models.Model):
    id = models.IntegerField(primary_key=True)
    venta = models.ForeignKey(Venta, db_column='venta')
    class Meta:
        db_table = 'venta_publico'

class VentaUsuarioSucursal(models.Model):
    id = models.IntegerField(primary_key=True)
    usuario_sucursal = models.ForeignKey(UsuarioSucursal, db_column='usuario_sucursal')
    venta = models.ForeignKey(Venta, db_column='venta')
    nombre_usuario = models.CharField(max_length=400L)
    class Meta:
        db_table = 'venta_usuario_sucursal'

