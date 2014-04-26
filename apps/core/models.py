from django.db import models
from django.db.models import Max 

class CategoriaProducto(models.Model):
    categoria = models.CharField(max_length=45L, db_column='Categoria', blank=True) # Field name made lowercase.
    class Meta:
        db_table = 'Categoria_producto'

#class Logged(models.Model):
#    session_key = models.CharField(max_length=100L, blank=True)
#    date = models.DateTimeField(null=True, blank=True)
#    access = models.CharField(max_length=45L, blank=True)
#    class Meta:#        db_table = 'Logged'

class Producto(models.Model):
    categoria_producto = models.ForeignKey(CategoriaProducto, db_column='categoria_producto') # Field name made lowercase.
    codigo = models.CharField(max_length=45L, blank=True)
    descripcion = models.CharField(max_length=45L, blank=True)
    class Meta:
        db_table = 'Producto'

class Rango(models.Model):
    min = models.IntegerField(null=True, db_column='Min', blank=True) # Field name made lowercase.
    max = models.IntegerField(null=True, db_column='Max', blank=True) # Field name made lowercase.
    class Meta:
        db_table = 'Rango'

class Sucursal(models.Model):
    nombre = models.CharField(max_length=150L, blank=True)
    estado = models.CharField(max_length=100L, blank=True)
    pais = models.CharField(max_length=50L, blank=True)
    tel = models.CharField(max_length=50L, blank=True)
    almacen_admipaq = models.CharField(max_length=100L, blank=True)
    iva = models.CharField(max_length=50L, blank=True)
    direccion = models.CharField(max_length=100L, blank=True)
    num_int = models.CharField(max_length=50L, blank=True)
    num_ext = models.CharField(max_length=45L, blank=True)
    folio_sucursal = models.CharField(max_length=50L, blank=True)
    descuento = models.CharField(max_length=10L, blank=True)
    class Meta:
        db_table = 'Sucursal'

class ClienteDatos(models.Model):
    nombre = models.CharField(max_length=100L, blank=True)
    telefono = models.CharField(max_length=100L, db_column='Telefono', blank=True) # Field name made lowercase.
    correo = models.CharField(max_length=100L, blank=True)
    pais = models.CharField(max_length=50L, blank=True)
    estado = models.CharField(max_length=50L, blank=True)
    municipio = models.CharField(max_length=45L, blank=True)
    sucursal = models.ForeignKey(Sucursal, db_column='sucursal') # Field name made lowercase.
    descuentos = models.CharField(max_length=45L, blank=True)
    class Meta:
        db_table = 'cliente_datos'

class ClienteFacturacion(models.Model):
    rfc = models.CharField(max_length=150L, blank=True)
    calle = models.CharField(max_length=150L, blank=True)
    colonia = models.CharField(max_length=150L, blank=True)
    num_int = models.CharField(max_length=45L, blank=True)
    num_ext = models.CharField(max_length=45L, blank=True)
    cod_postal = models.CharField(max_length=45L, blank=True)
    cliente_datos = models.ForeignKey(ClienteDatos , db_column = "cliente_datos")
    class Meta:
        db_table = 'cliente_facturacion'

class Eventos(models.Model):
    nombre_evento = models.CharField(max_length=45L, blank=True)
    class Meta:
        db_table = 'eventos'

class Log(models.Model):
    date = models.DateTimeField(null=True, blank=True)
    usuario = models.ForeignKey('Usuario')
    eventos = models.ForeignKey(Eventos)
    class Meta:
        db_table = 'log'

class inventario(models.Model):
    producto = models.ForeignKey(Producto, db_column='Producto_id') # Field name made lowercase.
    sucursal = models.ForeignKey(Sucursal, db_column='Sucursal_id') # Field name made lowercase.
    existencia = models.IntegerField(null=True, blank=True , db_column = "existencia")
    stock = models.IntegerField(null=True, blank=True , db_column = "stock")
    class Meta:
        db_table = 'inventario'

class venta(models.Model):
    sucursal = models.ForeignKey(Sucursal, db_column='Sucursal_id') # Field name made lowercase.
    fecha = models.DateTimeField( auto_now_add = True, db_column = "fecha" )


    folio = models.IntegerField( db_column = "folio")
    total = models.IntegerField( db_column = "total")
    total_productos = models.IntegerField( db_column = "total_productos")

    class Meta:
        db_table = 'venta'

    def save(self):
    	
	venta_qs = venta.objects.all().aggregate(Max('folio'))

	if venta_qs["folio__max"]:
		last = unicode(venta_qs ["folio__max"])
		self.folio = int(last)+1
	else:
		self.folio = 1
	

	super(venta , self).save()



class venta_has_producto(models.Model):

    venta = models.ForeignKey(venta, db_column='Venta_id') # Field name made lowercase.
    producto = models.ForeignKey(Producto, db_column='Producto_id') # Field name made lowercase.
    cantidad = models.IntegerField(null=True, blank=True , db_column = "cantidad")

    class Meta:
        db_table = 'venta_has_producto' 
	
	














class producto_has_rango(models.Model):
    producto = models.ForeignKey(Producto, db_column='Producto_id') # Field name made lowercase.
    rango = models.ForeignKey(Rango, db_column='rango') # Field name made lowercase.
    sucursal = models.ForeignKey(Sucursal, db_column='Sucursal_id') # Field name made lowercase.
    costo = models.IntegerField(null=True, blank=True , db_column = "costo")
    class Meta:
        db_table = 'producto_has_rango'


class Usuario(models.Model):
    nombre = models.CharField(max_length=500L, blank=True)
    rol = models.CharField(max_length=150L, blank=True)
    email = models.CharField(max_length=100L, blank=True)
    password = models.CharField(max_length=300L, blank=True)
    tel_cel = models.CharField(max_length=100L, blank=True)
    #logged = models.ForeignKey(Logged, db_column='Logged_id') # Field name made lowercase.

    class Meta:
        db_table = 'usuario'

class UsuarioHasSucursal(models.Model):
    usuario = models.ForeignKey(Usuario)
    Sucursal_id  = models.ForeignKey(Sucursal, db_column='Sucursal_id') # Field name made lowercase.
    class Meta:
        db_table = 'usuario_has_Sucursal'

class UsuarioSucursal(models.Model):
    tel_residencia = models.CharField(max_length=85L, blank=True)
    bono = models.CharField(max_length=45L, blank=True)
    porciento_comision = models.CharField(max_length=45L, blank=True)
    salario_real = models.CharField(max_length=45L, blank=True)
    num_seguro_social = models.CharField(max_length=100L, blank=True)
    direccion = models.CharField(max_length=200L, blank=True)
    nombre_aval = models.CharField(max_length=200L, blank=True)
    tel_aval = models.CharField(max_length=100L, blank=True)
    usuario = models.ForeignKey(Usuario)
    class Meta:
        db_table = 'usuario_sucursal'

class UsuarioSucursalHasSucursal(models.Model):
    usuario_sucursal = models.ForeignKey(UsuarioSucursal)
    sucursal = models.ForeignKey(Sucursal, db_column='Sucursal_id') # Field name made lowercase.
    class Meta:
        db_table = 'usuario_sucursal_has_Sucursal'

class Estados(models.Model):
	estado = models.CharField(max_length=60L)
	class Meta:
		db_table = 'estados'

class Municipios(models.Model):
    	estado = models.ForeignKey(Estados , db_column='estado') # Field name made lowercase.
	municipio = models.CharField(max_length=49L, blank=True)

	class Meta:
		db_table = 'municipios'

class VentaCliente(models.Model):
	cliente_datos = models.ForeignKey(ClienteDatos , db_column ="cliente_datos")
	venta = models.ForeignKey(venta, db_column = "venta")

	class Meta:
		db_table = 'venta_cliente'

class AsignacionSupervisorPlaza(models.Model):
    	usuario = models.ForeignKey('usuario' , db_column = "usuario")
	sucursal = models.ForeignKey(Sucursal, db_column='sucursal') 

	class Meta:
		db_table = 'asignacion_supervisor_plaza'


class VentaPublico(models.Model):
	venta = models.ForeignKey(venta, db_column = "venta")
	class Meta:
		db_table = 'venta_publico'


