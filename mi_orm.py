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

class CategoriaProducto(models.Model):
    id = models.IntegerField(primary_key=True)
    categoria = models.CharField(max_length=45L, db_column='Categoria') # Field name made lowercase.
    class Meta:
        db_table = 'categoria_producto'

class ClienteDatos(models.Model):
    id = models.IntegerField(primary_key=True)
    nombre = models.CharField(max_length=100L)
    telefono = models.CharField(max_length=100L, db_column='Telefono') # Field name made lowercase.
    correo = models.CharField(max_length=100L)
    pais = models.CharField(max_length=50L)
    estado = models.CharField(max_length=50L)
    municipio = models.CharField(max_length=45L)
    sucursal = models.IntegerField()
    descuentos = models.CharField(max_length=45L)
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
    cliente_datos = models.IntegerField()
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
    id = models.IntegerField()
    estado = models.CharField(max_length=60L)
    class Meta:
        db_table = 'estados'

class Eventos(models.Model):
    id = models.IntegerField(primary_key=True)
    nombre_evento = models.CharField(max_length=45L)
    class Meta:
        db_table = 'eventos'

class Inventario(models.Model):
    id = models.IntegerField()
    producto_id = models.IntegerField(db_column='Producto_id') # Field name made lowercase.
    sucursal_id = models.IntegerField(db_column='Sucursal_id') # Field name made lowercase.
    existencia = models.IntegerField(null=True, blank=True)
    stock = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = 'inventario'

class Log(models.Model):
    id = models.IntegerField(primary_key=True)
    date = models.DateTimeField(null=True, blank=True)
    usuario_id = models.IntegerField()
    eventos_id = models.IntegerField()
    class Meta:
        db_table = 'log'

class Municipios(models.Model):
    id = models.IntegerField(null=True, blank=True)
    estado = models.IntegerField(null=True, blank=True)
    municipio = models.CharField(max_length=49L, blank=True)
    class Meta:
        db_table = 'municipios'

class Producto(models.Model):
    id = models.IntegerField()
    categoria_producto = models.IntegerField()
    codigo = models.CharField(max_length=45L)
    descripcion = models.CharField(max_length=45L)
    class Meta:
        db_table = 'producto'

class ProductoHasRango(models.Model):
