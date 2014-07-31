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
    hora_entrada = models.DateTimeField( db_column = "hora_entrada", blank = True , null = True )


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
    fecha = models.DateTimeField( auto_now_add = True, db_column = "fecha" )
    usuario_creador = models.ForeignKey('Usuario' , db_column = "usuario_creador")
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
    total = models.FloatField( db_column = "total")
    total_productos = models.IntegerField( db_column = "total_productos")
    url_reporte =   models.CharField(max_length=500L, blank=True , db_column = "url_reporte")
    descuento_cliente =   models.CharField(max_length=500L, blank=True , db_column = "descuento_cliente")

    class Meta:
        db_table = 'venta'

    def save(self):
    
        venta_qs = venta.objects.all().filter(sucursal=self.sucursal).aggregate(Max('folio'))

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
    costo_por_producto = models.FloatField(null=True, blank=True , db_column = "costo_por_producto")

    class Meta:
        db_table = 'venta_has_producto' 


class producto_has_rango(models.Model):
    producto = models.ForeignKey(Producto, db_column='Producto_id') # Field name made lowercase.
    rango = models.ForeignKey(Rango, db_column='rango') # Field name made lowercase.
    sucursal = models.ForeignKey(Sucursal, db_column='Sucursal_id') # Field name made lowercase.
    costo = models.FloatField(null=True, blank=True , db_column = "costo")
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


class VentaUsuarioSucursal(models.Model):
    usuario_sucursal = models.ForeignKey(UsuarioSucursal , db_column = "usuario_sucursal")
    venta = models.ForeignKey(venta, db_column = "venta")
    nombre_usuario = models.CharField(max_length=400L)

    class Meta:
        db_table = 'venta_usuario_sucursal'


class Cambio(models.Model):

    sucursal = models.ForeignKey(Sucursal, db_column='sucursal') # Field name made lowercase.
    folio_ticket = models.TextField()
    fecha = models.DateTimeField( auto_now_add = True, db_column = "fecha" )
    modelo_entrada = models.TextField()
    modelo_salida = models.TextField()
    diferencia_precio = models.FloatField()
    motivo_cambio = models.TextField()
    cantidad_modelo_entrada = models.IntegerField()
    cantidad_modelo_salida = models.IntegerField()

    class Meta:
        db_table = 'cambio'


class AjusteInventario(models.Model):
    codigo = models.CharField(max_length=45L)
    sucursal = models.ForeignKey(Sucursal ,db_column = "sucursal") # Field name made lowercase.
    costo_publico = models.FloatField()
    faltante = models.IntegerField()
    sobrante = models.IntegerField()
    sistema = models.IntegerField()
    fisico = models.IntegerField()
    usuario = models.ForeignKey(Usuario , db_column = "usuario")
    fecha = models.DateTimeField( auto_now_add = True, db_column = "fecha" )
    class Meta:
        db_table = 'ajuste_inventario'





class Kardex(models.Model):

    fecha = models.DateTimeField( auto_now_add = True, db_column = "fecha" )
    folio = models.IntegerField()
    sucursal = models.ForeignKey(Sucursal, db_column='sucursal') # Field name made lowercase.
    tipo_registro = models.CharField(max_length=45L)
    inventario_inicial = models.IntegerField()
    entradas = models.IntegerField()
    salidas = models.IntegerField()
    existencia = models.IntegerField()
    descripcion = models.TextField()
    producto = models.ForeignKey(Producto, db_column='producto') # Field name made lowercase.

    class Meta:
        db_table = 'kardex'


class Bitacora(models.Model):

    sucursal = models.ForeignKey(Sucursal, db_column='sucursal') # Field name made lowercase.
    fecha = models.DateTimeField( auto_now_add = True, db_column = "fecha" )

    inicial =  models.IntegerField( default = 0)

    #Entradas
    entrada_compra_factura  = models.IntegerField( default = 0)
    entrada_cambios = models.IntegerField(default = 0)

    entrada_total = models.IntegerField( default = 0 )
 
    #SALIDAS
    salida_ventas = models.IntegerField( default = 0)

    salida_cambios = models.IntegerField( default = 0)
    salida_total = models.IntegerField( default = 0)
    disponible_fisico = models.IntegerField( default = 0)

    #SISTEMA
    sistema_existencia = models.IntegerField( default = 0)
    sistema_dif_ajustes = models.IntegerField( default = 0)
    sistema_cambios = models.IntegerField( default = 0)
    total_existencia = models.IntegerField( default = 0)

    diferencia = models.IntegerField( default = 0)

    #ventas efectivo
    ventas_publico = models.FloatField( default = 0)
    ventas_mayoreo = models.FloatField( default = 0)
    dep_en_facturas = models.FloatField( default = 0)
    gastos = models.FloatField( default = 0)
    total_a_depositar = models.FloatField( default = 0)


    class Meta:
        db_table = 'bitacora'


class CorteDia(models.Model):

    sucursal = models.ForeignKey(Sucursal, db_column='sucursal') # Field name made lowercase.
    usuario = models.ForeignKey(Usuario , db_column = "usuario")
    fecha = models.DateTimeField( auto_now_add = True, db_column = "fecha" )
    deposito_1 = models.FloatField()
    deposito_2 = models.FloatField()
    deposito_3 = models.FloatField()
    venta_mayoreo = models.FloatField()
    venta_publico = models.FloatField()
    total = models.FloatField()

    class Meta:
        db_table = 'corte_dia'

class GastosSucursal(models.Model):
    corte_dia = models.ForeignKey(CorteDia, db_column='corte_dia') # Field name made lowercase.
    fecha = models.DateTimeField( auto_now_add = True, db_column = "fecha" )
    gastos = models.FloatField()
    concepto = models.TextField()

    class Meta:
        db_table = 'gastos_sucursal'


class DepositosSucursal(models.Model):

    corte_dia = models.ForeignKey(CorteDia, db_column='corte_dia') # Field name made lowercase.
    deposito = models.FloatField()
    numero_cuenta = models.CharField(max_length=200L)
    referencia = models.CharField(max_length=150L)
    fecha = models.DateTimeField( auto_now_add = True, db_column = "fecha" )
    cantidad = models.FloatField()
    comentario = models.TextField()
    deposito_real = models.FloatField()
    numero_deposito = models.IntegerField()

    class Meta:
        db_table = 'depositos_sucursal'


class FacturarVenta(models.Model):

    sucursal = models.ForeignKey(Sucursal, db_column='sucursal') # Field name made lowercase.
    venta = models.ForeignKey(venta, db_column='venta') # Field name made lowercase.
    cliente = models.ForeignKey(ClienteDatos , db_column = "cliente")
    fecha = models.DateTimeField( auto_now_add = True, db_column = "fecha" )

    class Meta:
        db_table = 'facturar_venta'





class ConfiguracionComision(models.Model):

    sucursal = models.ForeignKey(Sucursal, db_column='sucursal' , related_name="sucursal" ) # Field name made lowercase.
    sucursal_comision = models.ForeignKey(Sucursal, db_column='sucursal_comision' , related_name = "sucursal_comision") # Field name made lowercase.
    usuario = models.ForeignKey(Usuario , db_column = "usuario" )
    porcentaje_comision_total = models.FloatField(null=True, blank=True)
    porcentaje_comision = models.FloatField(null=True, blank=True)

    class Meta:
        db_table = 'configuracion_comision'


class Paquetes(models.Model):
    producto = models.ForeignKey(Producto, db_column='producto') # Field name made lowercase.

    class Meta:
        db_table = 'paquetes'


class PaquetesHasProducto(models.Model):
    productos = models.ForeignKey(Producto, db_column='productos') # Field name made lowercase.
    paquetes = models.ForeignKey(Paquetes, db_column='paquetes') # Field name made lowercase.

    class Meta:
        db_table = 'paquete_has_producto'


class CargarFactura(models.Model):
    fecha = models.DateTimeField( auto_now_add = True, db_column = "fecha" )
    sucursal = models.ForeignKey(Sucursal, db_column='sucursal') # Field name made lowercase.
    numero_factura = models.CharField(max_length=45L)
    procesado = models.IntegerField( default = 0)

    class Meta:
        db_table = 'cargar_factura'


class FacturaHasProductos(models.Model):

    factura = models.ForeignKey(CargarFactura, db_column='factura') # Field name made lowercase.
    codigo = models.CharField(max_length=45L)
    cantidad_emitida   = models.IntegerField()
    procesado = models.IntegerField( default = 0)
    comentario = models.TextField( default = "" )
    cantidad_recibida = models.IntegerField( default = 0 )

    class Meta:
        db_table = 'factura_has_productos'

class CargarFacturaEnInventario(models.Model):
    sucursal = models.ForeignKey(Sucursal, db_column='sucursal') # Field name made lowercase.
    numero_factura = models.IntegerField(null=True, blank=True)
    procesada = models.IntegerField(null=True, blank=True)

    class Meta:
        db_table = 'cargar_factura_en_inventario'


class Asistencia(models.Model):
    fecha = models.DateTimeField( auto_now_add = True)
    usuario = models.ForeignKey(UsuarioSucursal , db_column = "usuario")
    sucursal = models.ForeignKey(Sucursal , db_column = "sucursal") # Field name made lowercase.

    class Meta:
        db_table = 'asistencia'


class StatusVentasAsistidas(models.Model):

    num_ventas_asistidas = models.IntegerField(null=True, blank=True,default=0)
    num_ventas_no_asistidas = models.IntegerField(null=True, blank=True,default=0)
    num_ventas_totales = models.IntegerField(null=True, blank=True,default=0)
    num_sucursales_asistiendo = models.IntegerField(null=True, blank=True,default=0)
    supervisor  = models.ForeignKey('Usuario' , db_column="supervisor_id")
    fecha = models.DateTimeField( auto_now_add = True)

    class Meta:
        db_table = 'status_ventas_asistidas'


class StatusVentasAsistidasHasVentas(models.Model):

    sucursal = models.ForeignKey(Sucursal, db_column='sucursal_id')# Field name made lowercase.
    status_ventas_asistidas = models.ForeignKey(StatusVentasAsistidas, db_column='status_ventas_asistidas_id') # Field name made lowercase.
    folio_venta = models.IntegerField( db_column="venta_id")
    tiempo_asistiendo = models.TextField(blank=True)
    observacion = models.TextField(blank=True)

    class Meta:
        db_table = 'status_ventas_asistidas_has_ventas'
