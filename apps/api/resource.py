#encoding:utf-8
from django.utils import timezone
from datetime import date , datetime , timedelta
from tastypie.authentication import BasicAuthentication
from django.db.models import Q , F
from tastypie.exceptions import *
import unicodedata
from django.core import serializers
import re
from tastypie import fields
from apps.core.models import *
from tastypie.exceptions import BadRequest
from tastypie.authorization import Authorization
from tastypie.resources import ModelResource , ALL , ALL_WITH_RELATIONS
from tastypie.exceptions import Unauthorized
from django.contrib.auth.models import User
from django.db.models import Q

MAYOREO_INT = 2
HORA_CENTRAL_MX = -5

class ISELAuthentication(Authorization):
	def create_list( self , object_list, bundle):
		raise Unauthorized("sorry, dont create")
	def is_authenticated( self , request , **kwargs ):
		return False

#************************************************************************************************************
#********************************************* bitacora Sucursal*******************************************
#************************************************************************************************************


class BitacoraResource(ModelResource):

	sucursal = fields.ForeignKey("apps.api.resource.SucursalSinInventarioResource", 'sucursal'    ,  null = True ,full = True )

	class Meta:
		queryset = Bitacora.objects.all()
		allowed_methods = ["get"]
		resource_name ='bitacora'
		authorization= Authorization()

		filtering  = {

			  "fecha" : ["lte","gte", "lt","gt"],
			  "sucursal" : ALL_WITH_RELATIONS,

			}

	def dehydrate(self , bundle ):

		return bundle


#************************************************************************************************************
#********************************************* Asistencia Sucursal*******************************************
#************************************************************************************************************


class AsistenciaResource(ModelResource):

	usuario = fields.ForeignKey("apps.api.resource.UsuarioSucursalResource", 'usuario'    ,  null = True , full = True )
	sucursal = fields.ForeignKey("apps.api.resource.SucursalSinInventarioResource", 'sucursal'    ,  null = True ,full = True )

	class Meta:
		queryset = Asistencia.objects.all()
		allowed_methods = ["get"]
		resource_name ='asistencia'
		authorization= Authorization()


		filtering  = {

			  "fecha" : ["lte","gte", "lt","gt"],
			  "sucursal" :ALL_WITH_RELATIONS,

			}


	def dehydrate(self , bundle ):

		#current_time_at_mx_zone = datetime.now()

		#hora de entrada de un usuario
		hora_entrada_usuario = bundle.data.get("fecha")

		hora_entrada_usuario_hora = hora_entrada_usuario.hour + HORA_CENTRAL_MX
		hora_entrada_usuario_minuto  = hora_entrada_usuario.minute


		#hora de entrada fijada en la sucursal
		hora_entrada_en_sucursal  = bundle.data.get("sucursal").data.get("hora_entrada")

		hora_entrada_en_sucursal_minuto = hora_entrada_en_sucursal.minute
		hora_entrada_en_sucursal_hora = hora_entrada_en_sucursal.hour


		minutos_diferencia = hora_entrada_usuario_minuto - hora_entrada_en_sucursal_minuto
		horas_diferencia = hora_entrada_usuario_hora - hora_entrada_en_sucursal_hora

		bundle.data["tiempo_retardo"] = "{0}hrs. - {1} Min.".format(horas_diferencia , minutos_diferencia) if horas_diferencia > 0 else  "{0} min.".format( minutos_diferencia )

		return bundle




#************************************************************************************************************
#********************************************* Usuario Sucursal *******************************************
#************************************************************************************************************


class UsuarioHasSucursalResource(ModelResource):

	usuario = fields.ForeignKey("apps.api.resource.UsuarioResource", 'usuario'    ,  null = True , full = True )
	Sucursal_id  = fields.ForeignKey("apps.api.resource.SucursalSinInventarioResource", 'Sucursal_id'    ,  null = True ,full = True )

	class Meta:
		queryset = UsuarioHasSucursal.objects.all()
		resource_name ='usuariohassucursal'
		authorization= Authorization()


		filtering  = {

			"usuario"  : ["exact"],

				}





#************************************************************************************************************
#********************************************* Estados  *******************************************
#************************************************************************************************************


class EstadosResource(ModelResource):

	class Meta:
		queryset = Estados.objects.all()

		resource_name ='estados'

#************************************************************************************************************
#********************************************* Municipios ***************************************************
#************************************************************************************************************


class MunicipioResource(ModelResource):
	estado = fields.ForeignKey(EstadosResource, 'estado'    ,  null = True )
	class Meta:
		queryset = Municipios.objects.all()
		resource_name ='municipios'

		filtering  = {

			"estado"  : ["exact"],

				}


#************************************************************************************************************
#********************************************* Categoria Producto *******************************************
#************************************************************************************************************


class CategoriaProductoResource(ModelResource):
    class Meta:
	    queryset = CategoriaProducto.objects.all()
	    resource_name ='categoriaproducto'
	    authorization= Authorization()


#************************************************************************************************************
#********************************************* Product ******************************************************
#************************************************************************************************************

class ProductoResource(ModelResource):

	categoria_producto = fields.ForeignKey(CategoriaProductoResource , 'categoria_producto'    , full = True , null = True )
	class Meta:
		queryset = Producto.objects.all()
		resource_name = 'producto'
		always_return_data = True
		authorization= Authorization()
		filtering = {

			"categoria" : ["exact"],
			"codigo" : ["icontains", "iexact"],

		}


#************************************************************************************************************
#*********************************************SUCURSAL ******************************************************
#************************************************************************************************************

class SucursalResource(ModelResource):

	inventario = fields.ToManyField('apps.api.resource.InventarioResource',

			attribute = lambda bundle:      inventario.objects.filter(sucursal = bundle.obj)

		, null = True , full = True		)

	class Meta:
		queryset = Sucursal.objects.all()
		resource_name = 'sucursal'
		authorization= Authorization()

		filtering = {
				"nombre" : ["icontains"]
			    }


	def obj_create(self, bundle, request=None, **kwargs):

		bundle = self.full_hydrate(bundle)
		bundle.obj.save()

		Bitacora.objects.create( sucursal = bundle.obj)

		return bundle



#************************************************************************************************************
#*********************************************Rango ******************************************************
#************************************************************************************************************

class RangoResource(ModelResource):

	class Meta:
		queryset = Rango.objects.all()
		resource_name = 'rango'
		authorization= Authorization()


#************************************************************************************************************
#*********************************************producto has rango  *******************************************
#************************************************************************************************************

class ProductoHasRangoesource(ModelResource):

	sucursal = fields.ForeignKey(SucursalResource, 'sucursal'     )
	producto = fields.ForeignKey(ProductoResource, 'producto' , full = True     )
	rango = fields.ForeignKey(RangoResource , 'rango'    , full = True , null = True )

	class Meta:
		always_return_data = True
		queryset = producto_has_rango.objects.all()
		resource_name = 'producto_has_rango'
		authorization= Authorization()

		filtering = {

			"producto" : ALL_WITH_RELATIONS,
			"sucursal" : ALL_WITH_RELATIONS,
			"rango" : ALL_WITH_RELATIONS



			}




#************************************************************************************************************
#*********************************************Sucursal Inventario  ******************************************
#************************************************************************************************************


class InventarioResource(ModelResource):
	""" Inventario de una sucursal."""

	sucursal = fields.ForeignKey("apps.api.resource.SucursalSinInventarioResource" , 'sucursal' , full = True     )
	producto = fields.ForeignKey(ProductoResource, 'producto' , full = True     )



	class Meta:
		queryset = inventario.objects.all()
		always_return_data = True
		resource_name = 'inventario'
		filtering = {
			  	"sucursal" : ["exact"],
			  	"producto" : ALL_WITH_RELATIONS
			  }
		authorization= Authorization()

	def dehydrate(self , bundle ):


		obj_producto = producto_has_rango.objects.filter( Q( sucursal = bundle.obj.sucursal ) , Q( producto = bundle.obj.producto) )
		producto_rango = []

		for rango_producto in obj_producto:
			producto_rango.append({ "id":  rango_producto.id  , "costo" : rango_producto.costo  ,  "producto" : "/api/v1/producto/{0}/".format( rango_producto.producto.id ) ,
						"rango" : {

							"id" : rango_producto.rango.id,
							"resource_uri" : "/api/v1/rango/{0}/".format(rango_producto.rango.id),
							"max" :  rango_producto.rango.max,
							"min" :  rango_producto.rango.min,

							} ,
						        "resource_uri" : "/api/v1/producto_has_rango/{0}/".format(rango_producto.id),
						        "sucursal": "/api/v1/sucursal/{0}/".format(rango_producto.sucursal.id)
						})

		bundle.data["producto_has_rango"] = producto_rango


		return bundle

	def obj_get_list(self , bundle , **kwargs):

		request = bundle.request

		querystring_get = dict(bundle.request.GET.iterlists())

		inventario_g = inventario.objects.all()

		if request.method == 'POST':
			return inventario_g


		try:
			codigo = querystring_get["codigo"] or False
		except:
			codigo = False

		if codigo :

			inventario_g = inventario_g.filter(producto__codigo__iexact  = codigo[0] )

		try:
			id_sucursal =  int(request.GET.get('sucursal'))
			return  inventario_g.filter( sucursal = id_sucursal)

			#return inventario_g.filter( id__in  =  id_inventario_g_sucursal)

		except:

			return inventario_g




class VentaResource(ModelResource):
	""" venta de una sucursal."""

	sucursal = fields.ForeignKey(SucursalResource, 'sucursal'     )
	producto = fields.ToManyField('apps.api.resource.VentaHasProductoResource',

			attribute = lambda bundle: venta_has_producto.objects.filter(venta = bundle.obj)

		, null = True , full = True)



	class Meta:
		queryset = venta.objects.all()
		resource_name = 'venta'
		filtering = { "sucursal" : ["exact"] , "folio" : ["exact"] }
		authorization= Authorization()
		always_return_data = True

	def dehydrate(self , bundle):
		#bundle.data["folio"] = bundle.obj.id
		#del bundle.data["producto"]

		return bundle


	def obj_create(self, bundle, request=None, **kwargs):
		""" se crea una venta """

		bundle = self.full_hydrate(bundle)
		productos = bundle.data["producto"]


		t = datetime.utcnow().strftime('%m_%d_%Y')

		name_sucursal = unicode(bundle.obj.sucursal.nombre.lower() )
		name_sucursal = unicodedata.normalize('NFKD', unicode(name_sucursal) ).encode('ascii', 'ignore').replace(" ","_").lower()




		name_utf8_decoded = name_sucursal #unicodedata.normalize('NFKD', unicode(bundle.obj.sucursal.nombre.lower().decode('utf-8') ) ).encode('ascii', 'ignore')



		bundle.obj.url_reporte = "{0}_{1}_.pdf".format( name_utf8_decoded , datetime.utcnow().strftime('%m_%d_%Y_%s') )
		bundle.obj.save()


		sucursal = bundle.obj.sucursal

		qs_usuariosucursal_has_sucursal = UsuarioHasSucursal.objects.filter( Sucursal_id  = sucursal)[0]
		current_user = qs_usuariosucursal_has_sucursal.usuario

		#instancia de usuario
		#current_user = qs_usuariosucursal_has_sucursal

		#instancia de usuario has sucursal
		current_user = UsuarioSucursal.objects.filter( usuario =  current_user )[0]



		#guarda el usuario_sucursal que hizo la venta
		VentaUsuarioSucursal.objects.create( usuario_sucursal = current_user , venta = bundle.obj , nombre_usuario =  current_user.usuario.nombre  )

		#se busca si la venta sera asignada aun cliente



		#id del cliente obtenido por parametro en body JSON
		id_cliente  = bundle.data["cliente"] or False

		#si existe un id guardamos la venta al cliente
		if id_cliente:

			#objeto del cliente
			obj_cliente  = ClienteDatos.objects.filter( id = id_cliente)[0]
			#se guarda la venta al cliente
			VentaCliente.objects.create( cliente_datos = obj_cliente , venta = bundle.obj )


		sucursal =   re.search('\/api\/v1\/sucursal\/(\d+)\/', str(bundle.data["sucursal"])).group(1)
		sucursal = Sucursal.objects.filter(id = sucursal)[0]

		range_products_by_sucursal = producto_has_rango.objects.filter(sucursal =  sucursal )

		#current time at now
		current_time = timezone.now() - timedelta(hours=5)
		year = current_time.year
		month = current_time.month
		day = current_time.day



		bitacora =  Bitacora.objects.filter( fecha__year = year , fecha__month = month , fecha__day = day , sucursal = sucursal )

		for producto in productos:

			id_producto =   re.search('\/api\/v1\/producto\/(\d+)\/', str(producto["producto"])).group(1)
			id_producto = Producto.objects.filter(id = id_producto)[0]
			cantidad = int(producto["cantidad"])

			#salida ventas para bitacoras
			salida_venta = bitacora[0].salida_ventas + cantidad
			bitacora.update( salida_ventas = salida_venta )

			#salidas_total en bitacora
			salida_total = bitacora[0].salida_total + cantidad
			bitacora.update( salida_total = salida_total )

			#decuenta el producto en venta al inventario de la sucursal actual

			existencia_producto_inventario = inventario.objects.filter ( producto = id_producto , sucursal = sucursal ).values("existencia")[0]["existencia"]

			nueva_existencia = (existencia_producto_inventario  - cantidad)



			inventario.objects.filter ( producto = id_producto , sucursal = sucursal ).update(existencia =   nueva_existencia  )

			#guardamos la venta en el kardex
			Kardex.objects.create( folio = bundle.obj.folio , sucursal = sucursal , tipo_registro = "TICKET" , inventario_inicial = 0L ,
						entradas = 0L , salidas = cantidad, existencia = existencia_producto_inventario , descripcion = "venta en sucursal" , producto = id_producto )



			#se busca el precio del control conforme al rango en el que se encuentre, este valor de guarda en venta_has_producto, que es a que precio se adquirio el producto
			cantidad_en_rango = 0L
			for product_range in range_products_by_sucursal:


				try:
					if  product_range.rango.min <= cantidad  and cantidad <= product_range.rango.max and product_range.producto.id == id_producto.id :

						cantidad_en_rango  = product_range.costo
						break
				except:
					raise NotFound("Error en rango, verifica que el producto tenga asignados todos los rangos")


			#guarda los productos dentro de la venta
			try:
				venta_has_producto.objects.create( venta = bundle.obj , producto = id_producto , cantidad = cantidad , costo_por_producto = cantidad_en_rango )
			except:
				raise NotFound("Error en rango, verifica que el producto tenga asignados todos los rangos")

		#se actualiza el disponible fisico de una sucursal
		update_disponible_fisico_in_bitacora(sucursal.id)
		calcular_ventas_totales(sucursal)

		return bundle




class VentaHasProductoResource(ModelResource):


	""" Los productos que se registran dentro de una venta de una sucursal."""

	venta = fields.ForeignKey(VentaResource, 'venta'  )
	producto = fields.ForeignKey(ProductoResource, 'producto' , full = True  )

	class Meta:
		queryset = venta_has_producto.objects.all()
		resource_name = 'ventahasproducto'
		filtering = { "sucursal" : ["exact"] }
		authorization= Authorization()

	#class SucursalInventarioResource(ModelResource):
	#""" Administrador de productos - El administrador de admisel puede modificar el rango y el stock de los productos
	#en las sucursales, no corresponde a la seccion de inventarios, esta seccion solo es para dar de alta un producto
	#asignarle el rango, y posteriormente asignarselo a una sucursal, para generar existencia, se hace a traves del cargo
	#de factura."""

	#sucursal = fields.ForeignKey(SucursalResource, 'sucursal'    , full = True , null = True )
	#producto = fields.ForeignKey(ProductoResource, 'producto'    , full = True , null = True )
	#rango = fields.ForeignKey(RangoResource , 'rango'    , full = True , null = True )
	#class Meta:
		#queryset = SucursalInventario.objects.all()
		#resource_name = 'adminproductos'
		#authorization= Authorization()



#************************************************************************************************************
#*********************************************   Cliente ****************************************************
#************************************************************************************************************


class ClienteResource(ModelResource):

	#cliente_facturacion = fields.ForeignKey(ClienteFacturacionResource , 'cliente_facturacion'    , full = True , null = True )
	sucursal = fields.ForeignKey(SucursalResource , 'sucursal'    , full = False , null = True )
	usuario_creador = fields.ForeignKey("apps.api.resource.UsuarioResource", 'usuario_creador'    , full = True , null = True )
	class Meta:

		allowed_methods = ['get',"post" ,"put" ]
		queryset = ClienteDatos.objects.all()
		resource_name = 'cliente'
		always_return_data = True
		authorization = Authorization()

		filtering = {

			  "nombre" : ["icontains"],


			  "fecha" : ["lte","gte", "lt","gt"],


			  "sucursal" : ["exact"],

			}


	def dehydrate(self , bundle ):

		cliente_datos = {}
		try:
			cliente_datos = ClienteFacturacion.objects.filter ( cliente_datos = bundle.obj )[0]
			bundle.data["datos_facturacion"] = cliente_datos.__dict__
			del bundle.data["datos_facturacion"]["_state"]
		except:
			bundle.data["datos_facturacion"] = {}



		return bundle



#************************************************************************************************************
#*********************************************Cliente Facturacion *******************************************
#************************************************************************************************************


class ClienteFacturacionResource(ModelResource):

	cliente_datos = fields.ForeignKey(ClienteResource, 'cliente_datos'    , full = False , null = True )
	class Meta:
		queryset = ClienteFacturacion.objects.all()
		resource_name = 'clientefacturacion'
		authorization= Authorization()

#************************************************************************************************************
#*********************************************Cliente Facturacion sin relacion ******************************
#************************************************************************************************************


class ClienteFacturacionSinRelacionResource(ModelResource):

	cliente_datos = fields.ForeignKey(ClienteResource, 'cliente_datos'    , full = False , null = True )
	class Meta:
		queryset = ClienteFacturacion.objects.all()
		resource_name = 'clientefacturacion'
		authorization= Authorization()



#************************************************************************************************************
#*********************************************Cliente Reporte  **********************************
#************************************************************************************************************


class ClienteReporteResource(ModelResource):

	sucursal = fields.ForeignKey(SucursalResource , 'sucursal'    , full = False , null = True )
	usuario_creador = fields.ForeignKey("api.resource.UsuarioResource", 'Usuario'    , full = False , null = True )


	cliente_datos_facturacion= fields.ToManyField('apps.api.resource.ClienteFacturacionSinRelacionResource',

			attribute = lambda bundle:      ClienteFacturacion.objects.filter(cliente_datos = bundle.obj)

		, null = True , full = True		)



	class Meta:
		queryset = ClienteDatos.objects.all().order_by("-fecha")
		resource_name = 'reportecliente'
		authorization= Authorization()

		filtering  = {

			"nombre"  : ["icontains"],

			 "fecha" : ["lte","gte", "lt","gt"],


				}







#************************************************************************************************************
#*********************************************   Logged ****************************************************
#************************************************************************************************************



#class LogeedResource(ModelResource):

#	class Meta:
#		queryset = Logged.objects.all()

#************************************************************************************************************
#*********************************************   Login ****************************************************
#************************************************************************************************************


class LoginResource(ModelResource):


	class Meta:
		excludes = ["password", "email" , "id" , "nombre" , "resource_uri" , "tel_cel"]
		queryset = Usuario.objects.all().distinct()
		allowed_methods = ['get' ]
		resource_name = 'login'
		limit = 1


	def dehydrate(self , bundle ):

		del bundle.data["resource_uri"]
		get_email= bundle.request.GET.get("email") or False
		get_password = unicode(bundle.request.GET.get("password"))

		user_exist = Usuario.objects.filter( Q(email = get_email ) , Q(password = get_password))

		if user_exist:


			bundle.data["usuario_resource_uri"] = "api/v1/usuario/{0}/".format( user_exist[0].id )
			bundle.data["loggin"] = True
			bundle.data["message"] = "201"
			bundle.data["nombre"] = user_exist[0].nombre

			if user_exist[0].rol == "sucursal":


				#bundle.data["info"] = UsuarioSucursal.objects.filter ( usuario = user_exist )
				UsuarioSucursalResponse = UsuarioSucursal.objects.filter ( usuario = user_exist )

				bundle.data["usuario_informacion"] =  {
					"salario_real":  UsuarioSucursalResponse[0].salario_real,
					"num_seguro_social": UsuarioSucursalResponse[0].num_seguro_social,
					"tel_aval": UsuarioSucursalResponse[0].tel_aval,
					"porciento_comision": UsuarioSucursalResponse[0].porciento_comision,
					"direccion": UsuarioSucursalResponse[0].direccion,
					"tel_residencia": UsuarioSucursalResponse[0].tel_residencia,
					"bono":UsuarioSucursalResponse[0].bono,
					"nombre_aval": UsuarioSucursalResponse[0].nombre_aval,

				}

				current_obj_sucursal_ = UsuarioHasSucursal.objects.select_related().filter( usuario = user_exist )[0].Sucursal_id
				bundle.data["sucursal"] =  current_obj_sucursal_.__dict__
				bundle.data["sucursal"].pop("_state")
				bundle.data["sucursal"]["resource_uri"] =   "api/v1/sucursal/{0}/".format( current_obj_sucursal_.id )
				bundle.data["rol"] = "sucursal"

				#pase de aistencia
				#checar si el usuario no ha pasado asistencia al iniciar secion

				year = date.today().year
				month = date.today().month
				day = date.today().day

				sucursal = Sucursal.objects.get(pk= current_obj_sucursal_.id )
				#calcular el total a facturar de ventas
				paso_asistencia = Asistencia.objects.filter( fecha__year = year , fecha__month = month , fecha__day = day ,  sucursal = sucursal , usuario = UsuarioSucursalResponse[0])
				pasa_asistencia = False if len(paso_asistencia) >  0  is not None else True

				if pasa_asistencia:
					Asistencia.objects.create( usuario = UsuarioSucursalResponse[0]  , sucursal = sucursal)
					#crea la bitacora para el dia de hoy, cuenta el producto inicial
					update_bitacora_by_sucursal_id(sucursal.id,contar_producto_inicial = True )


			if user_exist[0].rol == "supervisor":
				bundle.data["rol"] = "supervisor"


			if user_exist[0].rol == "foraneo":
				bundle.data["rol"] = "foraneo"


			if user_exist[0].rol == "administrador":
				bundle.data["rol"] = "administrador"


		else:

			bundle.data["loggin"] = False
			bundle.data["message"] = "Email o password incorrecto"
			del bundle.data["rol"]

		return bundle

	def alter_list_data_to_serialize(self, request, data):

		del data["meta"]
		return data


#************************************************************************************************************
#*********************************************   Usuario ****************************************************
#************************************************************************************************************



class UsuarioResource(ModelResource):

	"""
	Usuario - Datos del usuario
	"""

	nombre = fields.CharField(attribute='nombre')
	rol = fields.CharField(attribute='rol')
	#logged = fields.ForeignKey(LogeedResource, 'Logged'    , full = True , null = True )

	class Meta:
		always_return_data = True
		allowed_methods = ['get', 'post' , 'delete' , "put"]
		#excludes = ["password"]
		queryset = Usuario.objects.all().distinct()
		resource_name = 'usuario'
		authorization= ISELAuthentication()
		filtering  = {

			"nombre"  : ["icontains"],

				}



	def dehydrate(self , bundle ):

		current_obj = bundle.obj

		datos = []
		if bundle.obj.rol == "sucursal":

			try:
				datos = UsuarioSucursal.objects.filter(usuario = current_obj.id ) [0]

				UsuarioSucursalResponse = datos


				datos = {
						"salario_real":  UsuarioSucursalResponse.salario_real,
						"num_seguro_social": UsuarioSucursalResponse.num_seguro_social,
						"resource_uri": "/api/v1/usuariosucursal/{0}/".format(UsuarioSucursalResponse.id),
						"id": "{0}".format(UsuarioSucursalResponse.id),
						"tel_aval": UsuarioSucursalResponse.tel_aval,
						"porciento_comision": UsuarioSucursalResponse.porciento_comision,
						"direccion": UsuarioSucursalResponse.direccion,
						"tel_residencia": UsuarioSucursalResponse.tel_residencia,
						"bono":UsuarioSucursalResponse.bono,
						"nombre_aval": UsuarioSucursalResponse.nombre_aval,

					}

			except:
				datos = []



		keyword = User.objects.make_random_password()
		bundle.data["loggin"] = keyword
		bundle.data["datos"] = datos
		#del bundle.data["logged"]



		return bundle


	def obj_create(self , bundle , request = None , ):

		keyword = User.objects.make_random_password()
		#last_loggin = Logged.objects.create( session_key = keyword , access = True )
		#bundle.obj.logged  = last_loggin


		bundle = self.full_hydrate(bundle)
		bundle.obj.save()





		#Usuario.objects.update(pk = bundle.obj ).set(logged = last_loggin )


		return bundle



#************************************************************************************************************
#********************************************* Venta Cliente *******************************************
#************************************************************************************************************


class VentaClienteResource(ModelResource):

	venta = fields.ForeignKey( VentaResource , 'venta'     )
	cliente_datos = fields.ForeignKey(ClienteResource , 'cliente_datos'     )

	class Meta:
		queryset = VentaCliente.objects.all()
		resource_name ='ventacliente'
		authorization= Authorization()



#************************************************************************************************************
#********************************************* Asignacion supervisor plaza *********************************
#************************************************************************************************************


class AsignacionSupervisorPlazaResource(ModelResource):

	usuario = fields.ForeignKey("apps.api.resource.UsuarioResource", 'usuario'    ,  null = True, full = True )
	sucursal  = fields.ForeignKey("apps.api.resource.SucursalSinInventarioResource", 'sucursal'    ,  null = True, full = True )
	class Meta:
		queryset = AsignacionSupervisorPlaza.objects.all()
		resource_name ='asignacionsupervisorplaza'
		authorization= Authorization()

		filtering  = {

			"sucursal"  : ["exact"],

				}
#************************************************************************************************************
#********************************************* Venta Usuario Sucursal ***************************************
#************************************************************************************************************


class VentaUsuarioSucursalResource(ModelResource):

	venta = fields.ForeignKey(VentaResource, 'venta' , full = True  )
	usuario_sucursal = fields.ForeignKey("apps.api.resource.UsuarioSucursalResource" , 'usuario_sucursal' , null = True )

	class Meta:

		queryset = VentaUsuarioSucursal.objects.all()
		resource_name ='ventausuariosucursal'
		authorization= Authorization()


#************************************************************************************************************
#********************************************* Venta Publico ***********************************************
#************************************************************************************************************


class VentaPublicoResource(ModelResource):

	venta = fields.ForeignKey(VentaResource, 'venta' , full = True  )
	class Meta:
		queryset = VentaPublico.objects.all()
		resource_name ='ventapublico'
		authorization= Authorization()

#************************************************************************************************************
#*********************************************SUCURSAL SIN RELACIONEs  **************************************
#************************************************************************************************************
#Se creo este recurso porque el recurso principa de sucursal al incluirse SucursalResource regresa todo el inventario,
#en esta seccion no se requiere

class SucursalSinInventarioResource(ModelResource):

	class Meta:
		queryset = Sucursal.objects.all()



#************************************************************************************************************
#********************************************* Historial Venta ***********************************************
#************************************************************************************************************




class HistorialVentaResource(ModelResource):
	""" Historial de las ventas , se puede filtrar por sucursal."""

	sucursal = fields.ForeignKey(SucursalSinInventarioResource , 'sucursal' , full = True     )


	class Meta:
		allowed_methods = ['get' ]
		queryset = venta.objects.all().order_by('-fecha')
		resource_name = 'historialventa'
		filtering = {

		"sucursal" : ALL_WITH_RELATIONS,
		#"usuario" : ["iexact"],
		"fecha" : ["lte","gte", "lt","gt"],
		}

	def dehydrate(self , bundle):

		id_current_obj = bundle.obj.id
		try:
			VentaUsuarioSucursalQS = VentaUsuarioSucursal.objects.filter( venta__id = id_current_obj)[0]
			bundle.data["vendedor_sucursal"] =  VentaUsuarioSucursalQS.usuario_sucursal.usuario.nombre

		except:
			bundle.data["vendedor_sucursal"] = "sin asignar"


		try:
			ClienteVentaQuerySet = VentaCliente.objects.select_related().filter( venta__id  = id_current_obj )[0]
			nombre_cliente = ClienteVentaQuerySet.cliente_datos.nombre
			bundle.data["nombre_comprador"] =  ( nombre_cliente , "publico")[ not nombre_cliente]
		except :
			bundle.data["nombre_comprador"] =  "publico"



		return bundle

	def obj_get_list(self , bundle , **kwargs):


		request = bundle.request
		querystring_get = dict(bundle.request.GET.iterlists())




		ventas = venta.objects.all().order_by('-fecha')

		try:
			id_sucursal  = querystring_get["sucursal__in"] or False
		except:
			id_sucursal = False

		if id_sucursal:

			ventas = ventas.filter(sucursal__in = id_sucursal )


		try:
			user_id =  int(request.GET.get('usuario'))
			venta_usuario_sucursal = VentaUsuarioSucursal.objects.filter( usuario_sucursal__usuario  = user_id)
			id_ventas = []


			for ventas_el  in venta_usuario_sucursal:
				id_ventas.append( ventas_el.venta_id)

			return ventas.filter( id__in  =  id_ventas)

		except:

			return ventas



#************************************************************************************************************
#********************************************* Usuario Sucursal *******************************************
#************************************************************************************************************


class UsuarioSucursalResource(ModelResource):

	usuario = fields.ForeignKey("apps.api.resource.UsuarioResource", 'usuario'    ,  null = True , full = True )
	class Meta:
		queryset = UsuarioSucursal.objects.all()
		resource_name ='usuariosucursal'
		authorization= Authorization()




#************************************************************************************************************
#********************************************* reporte cambio  ***********************************************
#************************************************************************************************************




class CambioResource(ModelResource):
	""" Reporte de los cambios realizados en la sucursales """

	sucursal = fields.ForeignKey(SucursalSinInventarioResource , 'sucursal' , full = True     )


	class Meta:
		allowed_methods = ['get' , 'post' ]
		queryset = Cambio.objects.all().order_by('-fecha')
		resource_name = 'productocambio'
		filtering = {

		"sucursal" : ALL_WITH_RELATIONS,
		"fecha" : ["lte","gte", "lt","gt"],
		"modelo_entrada" : ["icontains","iexact"],
		"folio_ticket" : ["iexact"],

		}

		authorization= Authorization()


	def obj_create(self, bundle, request=None, **kwargs):

		bundle = self.full_hydrate(bundle)

		modelos_entrada = bundle.data.get("entrada")
		modelos_salida = bundle.data.get("salida")

		len_cantidad_modelo_salida =  sum([ modelo.get("cantidad") for modelo in modelos_salida] ) 
		len_cantidad_modelo_entrada = sum([ modelo.get("cantidad") for modelo in modelos_entrada] ) 

		if len(modelos_entrada)<=1:

			bundle.obj.modelo_entrada = ",".join( [ modelo.get("modelo_entrada")  for modelo in modelos_entrada ]) 
		else:
			bundle.obj.modelo_entrada = ",".join( [ ( ( modelo.get("modelo_entrada") + "," ) * modelo.get("cantidad") )[:-1]  for modelo in modelos_entrada ]) 

		if len(modelos_salida)<= 1:

			bundle.obj.modelo_salida = ",".join( [  modelo.get("modelo_salida")  for modelo in modelos_salida ]) 
		else:
			bundle.obj.modelo_salida = ",".join( [ ( ( modelo.get("modelo_salida") + "," ) * modelo.get("cantidad") )[:-1]  for modelo in modelos_salida ]) 

		bundle.obj.cantidad_modelo_salida = len_cantidad_modelo_salida 
		bundle.obj.cantidad_modelo_entrada = len_cantidad_modelo_entrada 

		bundle.obj.save()

		#current time at now
		current_time = timezone.now() - timedelta(hours=5)
		year = current_time.year
		month = current_time.month
		day = current_time.day

		bitacora = Bitacora.objects.filter( fecha__year = year , fecha__month = month , fecha__day = day , sucursal = bundle.obj.sucursal )

		#sumar los modelos de entrada al inventario
		total_productos_entrada_inventario =  0
		for _modelo_entrada in  modelos_entrada:

			_modelo_entrada_str = _modelo_entrada.get("modelo_entrada") 
			modelo_entrada_ = inventario.objects.filter( producto__codigo =  _modelo_entrada_str )
			nueva_existencia = modelo_entrada_[0].existencia + _modelo_entrada.get("cantidad")      
			total_productos_entrada_inventario += _modelo_entrada.get("cantidad")
			print modelo_entrada_[0].existencia , _modelo_entrada.get("cantidad") , nueva_existencia
			modelo_entrada_.update( existencia = nueva_existencia )


			#guardamos la venta en el kardex
			Kardex.objects.create( folio = bundle.obj.folio_ticket , sucursal = bundle.obj.sucursal , tipo_registro = "CAMBIO" , inventario_inicial = 0L ,
			 entradas = _modelo_entrada.get("cantidad")   , salidas = 0L , existencia = nueva_existencia , descripcion = "cambio de producto entrada" , producto = modelo_entrada_[0] )




		print total_productos_entrada_inventario
		#productos que estan entrando por cambios
		entrada_cambio_bitacora = bitacora[0].entrada_cambios + total_productos_entrada_inventario
		bitacora.update( entrada_cambios = entrada_cambio_bitacora  )


		total_productos_salida_inventario =  0
		#restar los modelos de salida al inventario
		for _modelo_salida in  modelos_salida:

			_modelo_salida_str = _modelo_salida.get("modelo_salida") 
			modelo_salida_ = inventario.objects.filter( producto__codigo =  _modelo_salida_str )
			nueva_existencia = modelo_salida_[0].existencia -  _modelo_salida.get("cantidad")      

			total_productos_salida_inventario += _modelo_salida.get("cantidad") 
			print modelo_salida_[0].existencia , _modelo_salida.get("cantidad") , nueva_existencia
			modelo_salida_.update( existencia = nueva_existencia )


			#guardamos la venta en el kardex
			Kardex.objects.create( folio = bundle.obj.folio_ticket , sucursal = bundle.obj.sucursal , tipo_registro = "CAMBIO" , inventario_inicial = 0L ,
			 entradas = 0L , salidas = _modelo_salida.get("cantidad")  , existencia = nueva_existencia , descripcion = "cambio de producto salida " , producto = modelo_salida_[0] )



		#producto que estan saliendo por cambios
		salida_cambio_bitacora = bitacora[0].salida_cambios + total_productos_salida_inventario
		bitacora.update( salida_cambios = salida_cambio_bitacora )


		#producto que estan entrando en total por cambios
		entrada_total = bitacora[0].entrada_total + total_productos_entrada_inventario
		bitacora.update( entrada_total = entrada_total )


		#salidas_total en bitacora
		salida_total = bitacora[0].salida_total +  total_productos_salida_inventario
		bitacora.update( salida_total = salida_total )


		#se actualiza el disponible fisico de una sucursal
		update_disponible_fisico_in_bitacora(bundle.obj.sucursal.id)

		update_bitacora_existencias_de_sistema( bundle.obj.sucursal.id )

		return bundle




#************************************************************************************************************
#********************************************* Ajuste Inventario ***********************************************
#************************************************************************************************************




class ReporteAjusteInventarioResource(ModelResource):
	"""Reporte en Administrador/supervisor : Consume la informacion del inventario que las sucursales hacen semanalmente
	  Sucursales : Ingresan el inventario semanalmente por producto
	
	"""

	sucursal = fields.ForeignKey(SucursalSinInventarioResource , 'sucursal' , full = True, null = False )
	usuario = fields.ForeignKey(UsuarioResource, 'usuario' , full = True)


	class Meta:
		always_return_data = True
		allowed_methods = ['get' , 'post' ]
		#excludes = ["sobrante", "faltante" , "fecha" ,  "sistema" , "costo_publico"]
		queryset = AjusteInventario.objects.all().order_by('-fecha')
		resource_name = 'ajusteinventario'
		filtering = {

				"sucursal" : ["exact"],
				"usuario" : ["exact"],
				"fecha" : ["lte","gte", "lt","gt"],

		}

		authorization= Authorization()

	def dehydrate(self , bundle):
		_codigo_producto = bundle.data["codigo"]
		_sucursal = bundle.data["sucursal"].obj

		producto_in_inventairo = inventario.objects.all().filter( sucursal = _sucursal.id , producto__codigo = _codigo_producto  )[0]

		bundle.data["id_inventario_en_producto"] = producto_in_inventairo.id
		return bundle




	def obj_create(self, bundle, request=None, **kwargs):
		""" Se hace un ajuste de inventario por una sucursal semanalmente """

		try:
			bundle = self.full_hydrate(bundle)
			codigo = bundle.data["codigo"]
			fisico = int(bundle.data["fisico"] )

			sucursal_ =   re.search('\/api\/v1\/sucursal\/(\d+)\/', str(bundle.data["sucursal"])).group(1)
			usuario = re.search('\/api\/v1\/usuario\/(\d+)\/', str(bundle.data["usuario"])).group(1)

			#obtenemos el producto filtrado por la sucursal y el codigo exacto ignoring case

			current_product = inventario.objects.filter( Q(producto__codigo__iexact = codigo ) , Q(sucursal__id   = sucursal_ ) )[0]

			#cantidad en el sistema
			existencia_current_product_in_system = int(current_product.existencia)


			bundle.obj.sistema = existencia_current_product_in_system

			#productos faltantes
			faltante = ( existencia_current_product_in_system - fisico )

			if faltante <= 0:
					faltante = 0

			bundle.obj.faltante = faltante


			sobrante = ( fisico - existencia_current_product_in_system)
			# si hay productos sobrantes
			if  sobrante > 0:

				bundle.obj.sobrante = sobrante
			else:

				bundle.obj.sobrante = 0


			if faltante > 0 :

				current_product =  current_product.producto
				try:

					current_rango = producto_has_rango.objects.filter( producto =   current_product.id , rango__min = 1, rango__max = 1 , sucursal  = sucursal_ )[0]

				except Exception as error:

					current_rango = producto_has_rango.objects.filter( producto =   current_product , rango__min = 1, rango__max = 1 , sucursal  = bundle.obj.sucursal )

				deuda = current_rango.costo * faltante

				bundle.obj.costo_publico = deuda
			else:
				bundle.obj.costo_publico = 0

			bundle.obj.save()

			return bundle

		except:
			raise NotFound("Error al intentar hacer el ajuste, verifica el codigo del producto, id sucursal , id_usuario")
			return bundle



#************************************************************************************************************
#********************************************* reporte Inventario Existencias  ***********************************************
#************************************************************************************************************




class ReporteInventarioResource(ModelResource):
	""" Existencia de productos en Inventario de una sucursal."""

	sucursal = fields.ForeignKey(SucursalResource, 'sucursal'  )
	producto = fields.ForeignKey(ProductoResource, 'producto' , null = True, full = True )



	class Meta:
		queryset =  inventario.objects.all()
		allowed_methods = ['get' ]
		resource_name = 'reporteexistencia'
		filtering = {
			  	"sucursal" : ["exact"],
			  	"producto" : ["exact"],
			  }
		authorization= Authorization()
		#authorization= BasicAuthentication()

	def dehydrate(self , bundle):
		bundle.data["sucursal_codigo"] = bundle.obj.sucursal.almacen_admipaq
		bundle.data["sucursal_nombre"] = bundle.obj.sucursal.nombre
		return bundle



	#def alter_list_data_to_serialize(self, request, data):
	#	inv = inventario.objects.all().values("sucursal","existencia","sucursal__almacen_admipaq").distinct()
	#	return data







#************************************************************************************************************
#*********************************************Reporte Inventario General  **********************************
#************************************************************************************************************


class KardexResource(ModelResource):
	""" Kardex : este se puede usar en la seccion de inventario general ."""

	sucursal = fields.ForeignKey("apps.api.resource.SucursalSinInventarioResource" , 'sucursal' , full = True     )
	producto = fields.ForeignKey(ProductoResource, 'producto' , full = True     )


	class Meta:
		allowed_methods = ["get"]
		queryset = Kardex.objects.all()
		always_return_data = True
		resource_name = 'kardex'
		filtering = {
			  	"sucursal" : ["exact"],
			  	"producto" : ["exact"],
			 	"fecha" : ["lte","gte", "lt","gt"],
			  }
		authorization= Authorization()



#************************************************************************************************************
#********************************************* Corte dia ************************************************
#************************************************************************************************************


class CorteDiaResource(ModelResource):

	""" Corte del dia de una sucursal """

	sucursal = fields.ForeignKey("apps.api.resource.SucursalSinInventarioResource" , 'sucursal' , full = True     )
	usuario = fields.ForeignKey("apps.api.resource.UsuarioResource", 'usuario'    ,  null = True , full = True )


	class Meta:
		allowed_methods = ["get", "post" , "put" , "delete"]
		queryset = CorteDia.objects.all()
		always_return_data = True
		resource_name = 'cortedia'
		filtering = {
			  	"sucursal" : ALL_WITH_RELATIONS ,
			  	"usuario" : ["exact"],
			 	"fecha" : ["lte","gte", "lt","gt"],
			  }
		authorization= Authorization()


	def obj_create(self, bundle, request=None, **kwargs):

		bundle = self.full_hydrate(bundle)


		sucursal =   re.search('\/api\/v1\/sucursal\/(\d+)\/', str(bundle.data["sucursal"])).group(1)

		#el ultimo corte del dia
		try:
			fecha_ultimo_corte = CorteDia.objects.filter( sucursal  = sucursal ).order_by("-id")[0].fecha

			FacturarVenta_qs =    FacturarVenta.objects.filter ( fecha__gt  = fecha_ultimo_corte ,  sucursal = sucursal)
			id_venta_facturacion = FacturarVenta_qs.values("id")

			ventas_desde_ultimo_corte = venta.objects.filter( fecha__gt  = fecha_ultimo_corte , sucursal = sucursal ).exclude( id__in = id_venta_facturacion )
			ventas_hoy = ventas_desde_ultimo_corte

		except:
			#si es el primer corte del dia

			current_time = timezone.now()
			#calcular el total a facturar de ventas
			FacturarVenta_qs =    FacturarVenta.objects.filter ( fecha__lte = current_time,   sucursal = sucursal)
			id_venta_facturacion = FacturarVenta_qs.values("id")

			#ventas totales diarias  por sucursal objectos
			ventas_hoy = venta.objects.filter( fecha__lte = current_time ,  sucursal = sucursal ).exclude( id__in = id_venta_facturacion )




		ventas_hoy_total = 0

		#ventas totales a publico por sucursal
		ventas_hoy_publico =0  #VentaPublico.objects.filter( venta__fecha__year = year , venta__fecha__month = month , venta__fecha__day = day , venta__sucursal = sucursal )

		#ventas totales a mayoreo por sucursal
		ventas_hoy_mayoreo = 0
		for venta_ in ventas_hoy:

			ventas_hoy_total+= venta_.total

			if venta_.total_productos >= MAYOREO_INT:
				ventas_hoy_mayoreo+= venta_.total
			else:
				ventas_hoy_publico+=venta_.total


		ventas_facturas = 0


		for venta_a_facturar in FacturarVenta_qs:
			ventas_facturas	 +=  venta_a_facturar.venta.total

		ventas_hoy_total_con_factura = ventas_hoy_total

		#total de la venta incluyendo facturas
		#ventas_hoy_total_con_factura += ventas_facturas

		bundle.obj.deposito_1 =  ventas_hoy_total * .60
		bundle.obj.deposito_2 =  ventas_hoy_total * .40
		bundle.obj.deposito_3 =  ventas_facturas
		bundle.obj.venta_mayoreo = ventas_hoy_mayoreo
		bundle.obj.venta_publico = ventas_hoy_publico
		bundle.obj.total =  ventas_hoy_total_con_factura

		bundle.obj.save()


		return bundle


	def dehydrate(self , bundle ):

		return bundle






#************************************************************************************************************
#********************************************* gastos sucursal************************************************
#************************************************************************************************************


class SucursalGastosResource(ModelResource):
	""" Gastos sucursal: Ingresar o ver los gastos de una sucursal """
	corte_dia = fields.ForeignKey(CorteDiaResource, 'corte_dia' , full = False)

	class Meta:
		allowed_methods = ["get", "post" , "put" , "delete" ]
		queryset = GastosSucursal.objects.all()
		always_return_data = True
		resource_name = 'sucursalgastos'
		filtering = {
			  	"corte_dia" : ALL_WITH_RELATIONS,
			  }
		authorization= Authorization()

	def dehydrate(self , bundle ):

		return bundle




#************************************************************************************************************
#********************************************* Deposito sucursal************************************************
#************************************************************************************************************


class DepositoSucursalResource(ModelResource):
	""" Deposito reportado por sucursal: """
	corte_dia = fields.ForeignKey(CorteDiaResource, 'corte_dia' , full = False)

	class Meta:
		allowed_methods = ["get", "post"]
		queryset = DepositosSucursal.objects.all()
		always_return_data = True
		resource_name = 'depositosucursal'
		filtering = {
			  	"corte_dia" : ALL_WITH_RELATIONS,
				"fecha" : ["lte","gte", "lt","gt"],
			  }
		authorization= Authorization()



#************************************************************************************************************
#********************************************* Facturar venta sucursal***********************************
#************************************************************************************************************


class FacturarVentaResource(ModelResource):
	""" supervisor - Reporte para facturar una venta ,  sucursal - enviar que venta se requiere facturar"""

	sucursal = fields.ForeignKey(SucursalSinInventarioResource, 'sucursal' , full = True     )
	cliente = fields.ForeignKey(ClienteResource, 'cliente'    , full = True , null = True )
	venta = fields.ForeignKey(VentaResource, 'venta' , full = True  )


	class Meta:
		allowed_methods = ["get", "post"]
		queryset = FacturarVenta.objects.all()
		always_return_data = True
		resource_name = 'facturarventa'
		filtering = {
			  	"venta" : ALL_WITH_RELATIONS,
			  	"cliente" : ALL_WITH_RELATIONS,
			  	"sucursal" : ALL_WITH_RELATIONS,
			  }
		authorization= Authorization()






#************************************************************************************************************
#*********************************************  ConfiguracionComision    ***********************************
#************************************************************************************************************


class ConfiguracionComisionResource(ModelResource):
	"""Configuracion de comision para usuarios en sucursales"""

	sucursal = fields.ForeignKey(SucursalSinInventarioResource, 'sucursal' , full = True     )
	sucursal_comision = fields.ForeignKey(SucursalSinInventarioResource, 'sucursal_comision' , full = True     )

	usuario = fields.ForeignKey("apps.api.resource.UsuarioResource", 'usuario'    ,  null = True , full = True )

	class Meta:
		allowed_methods = ["get", "post" , "put", "delete"]
		queryset = ConfiguracionComision.objects.all()
		always_return_data = True
		resource_name = 'configuracioncomision'
		filtering = {
			  	"sucursal" : ALL_WITH_RELATIONS,
			  	"usuario" : ALL_WITH_RELATIONS,
			  	"sucursal_comision" : ALL_WITH_RELATIONS,
			  }
		authorization= Authorization()




#************************************************************************************************************
#*********************************************  Paquetes ***********************************
#************************************************************************************************************


class PaquetesResource(ModelResource):
	"""Paquetes """
	producto = fields.ForeignKey(ProductoResource, 'producto' , full = True     )

	class Meta:
		allowed_methods = ["get", "post"]
		queryset = Paquetes.objects.all()
		always_return_data = True
		resource_name = 'paquete'
		filtering = {
			  	"producto" : ALL_WITH_RELATIONS,
			  }

		authorization= Authorization()


	def dehydrate(self , bundle ):

		obj_paquete = PaquetesHasProducto.objects.filter( paquetes = bundle.obj )

		producto = []

		for producto_ in obj_paquete:

			producto.append({
						       "id":  producto_.productos.id  ,
						       "resource_uri" : "/api/v1/producto/{0}/".format(producto_.productos.id),
						       "codigo": producto_.productos.codigo
						})

		try:
			del bundle.data["productos_paquete" ]
		except:
			pass
		bundle.data["productos_paquete" ] =  producto

		return bundle



	def obj_create(self, bundle, request=None, **kwargs):

		bundle = self.full_hydrate(bundle)

		_current_id_paquete = re.search('\/api\/v1\/producto\/(\d+)\/', str(bundle.data["producto"])).group(1)
		bundle.obj.producto.id = _current_id_paquete

		bundle.obj.save()

		_current_paquete = bundle.obj

		#save m2m relationship data
		_productos = bundle.data["productos_paquete"]

		_control_remoto_en_paquete = []

		#asignacion de todos los productos que conteiene el paquete
		for key , _producto in enumerate(_productos):


			id_producto =   re.search('\/api\/v1\/producto\/(\d+)\/', str(_producto["producto"])).group(1)
			id_producto = Producto.objects.filter(id = id_producto)[0]

			#se obtiene el paquete el control remot en la primera posicion
			if key == 0:
				_control_remoto_en_paquete = id_producto


			product_in_paquete = PaquetesHasProducto.objects.create( paquetes = _current_paquete , productos = id_producto )

		#bundle.data["all_productos_in_paquete"] = _all_products

		#asignacion de todos los rangos que tiene el control remoto al paquete acutal
		#rango_control_remoto_en_paquete = producto_has_rango.objects.filter( producto = _control_remoto_en_paquete )



		return bundle

#************************************************************************************************************
#*********************************************  Cargar Factura **********************************************
#************************************************************************************************************


class CargarFacturaResource(ModelResource):
	"""Cargar factura """
	sucursal = fields.ForeignKey(SucursalResource, 'sucursal'     )
	codigo = fields.ToManyField('apps.api.resource.CargarFacturaHasProductosResource',

			attribute = lambda bundle: FacturaHasProductos.objects.filter(factura = bundle.obj)

		, null = True , full = True)


	class Meta:

		allowed_methods = ["get", "post" , "put", "delete"]
		queryset = CargarFactura.objects.all()
		always_return_data = True
		resource_name = 'cargarfactura'
		filtering = {
				"fecha" : ["lte","gte", "lt","gt"],
			  	"sucursal" : ["exact"],
			  	"numero_factura" : ["exact"],
			  }
		authorization= Authorization()

	def obj_create(self, bundle, request=None, **kwargs):

		bundle = self.full_hydrate(bundle)

		bundle.obj.save()

		factura = bundle.obj

		#_current_id_factura  = re.search('\/api\/v1\/producto\/(\d+)\/', str(bundle.data["producto"])).group(1)
		codigos_  = bundle.data["codigo"]
		for codigo in codigos_:
			FacturaHasProductos.objects.create(factura = factura , cantidad_emitida = codigo["cantidad_emitida"] , codigo = codigo["codigo"] )

		return bundle


#*********************************************  Cargar  Factura has productos  ******************************
#************************************************************************************************************


class CargarFacturaHasProductosResource(ModelResource):
	"""Cargar factura has productos  """

	class Meta:
		allowed_methods = ["get", "post" , "put", "delete"]
		queryset = FacturaHasProductos.objects.all()
		resource_name = 'productosfactura'
		always_return_data = True
		authorization= Authorization()

#*********************************************  Cargar  Factura en un inoventario de una sucursal     ******
#************************************************************************************************************



class CargarFacturaEnInventarioResource(ModelResource):
	""" Inventario de una sucursal actualizado por una facutra en el sucursal."""

	sucursal = fields.ForeignKey("apps.api.resource.SucursalSinInventarioResource" , 'sucursal' , full = True     )

	class Meta:
		queryset = CargarFacturaEnInventario.objects.all()
		always_return_data = True
		resource_name = 'cargarfacturainventario'
		filtering = {
			  	"sucursal" : ["exact"],
			  	"numero_factura" : ["exact"],
			  }
		authorization= Authorization()

	def obj_create(self, bundle, request=None, **kwargs):

		bundle = self.full_hydrate(bundle)
		bundle.obj.procesada = 1
		bundle.obj.save()

		#carga los nuevos productos en el inventairo de una factura
		if bundle.data["procesada"]:

			factura_id =  bundle.data["numero_factura"]
			sucursal_id = re.search('\/api\/v1\/sucursal\/(\d+)\/', str(bundle.data["sucursal"])).group(1)

			try:

				factura_instance = factura_data  = CargarFactura.objects.filter( sucursal = sucursal_id , procesado = 0 , numero_factura = factura_id  )


				#productos dentro de una factura que se van a iterar y buscar en el inventario de la sucursal para actualizar los datos
				Productos_factura = FacturaHasProductos.objects.filter ( factura = factura_data[0] )
				print Productos_factura



				for _producto_in_factura in Productos_factura:

					_codigo_producto  = _producto_in_factura.codigo
					print _codigo_producto

					_current_producto_en_inventario =  qs_producto_en_inventario  = inventario.objects.filter(
							sucursal  = sucursal_id, producto__codigo  = _codigo_producto )

					print _codigo_producto ,_current_producto_en_inventario

					#guardamos la venta en el kardex
					_tmp_obj_prod_  = _current_producto_en_inventario[0]

					Kardex.objects.create( folio = factura_id , sucursal = _tmp_obj_prod_.sucursal , tipo_registro = "FACTURA" , inventario_inicial = 0L ,

			 		entradas = _producto_in_factura.cantidad_emitida  , salidas = 0L , existencia = _tmp_obj_prod_.existencia, descripcion = "Cargar producto de factura en inventario" , 

					producto = _tmp_obj_prod_.producto )
					#end guardamos la venta en el kardex


					_current_producto_en_inventario = _current_producto_en_inventario_instance  = qs_producto_en_inventario

					_current_producto_en_inventario = _current_producto_en_inventario[0]

					#existencia del producto en inventario
					_current_existencia_in_producto  = _current_producto_en_inventario.existencia

					#se suma la existencia mas los productos que se enviaron por una factura
					_existencia_total = _current_existencia_in_producto + _producto_in_factura.cantidad_emitida
					_current_producto_en_inventario_instance.update( existencia = _existencia_total )

					#actualizamos la existencia del inventario

					factura_instance.update( procesado = 1 )
					update_bitacora_by_sucursal_id(sucursal_id)

					#se actualiza el disponible fisico de una sucursal
					update_disponible_fisico_in_bitacora(sucursal_id)

				return bundle

			except Exception as error:
				raise NotFound( error )




def update_bitacora_by_sucursal_id(sucursal_id ,contar_producto_inicial = False ):

	#current time at now
	current_time = timezone.now() - timedelta(hours=5)
	year = current_time.year
	month = current_time.month
	day = current_time.day



	bitacora = bitacora_qs  = Bitacora.objects.filter( fecha__year = year , fecha__month = month , fecha__day = day , sucursal = sucursal_id )
	#se creaa una bitacora para el dia de hoy
	if len(bitacora) is 0 :
		bitacora = Bitacora.objects.create( sucursal_id  = sucursal_id )
		bitacora = Bitacora.objects.filter( id = bitacora.id )
	else:
		#la bitacora ya existia para el dia de hoy
		pass

	#contar todo el producto inicial de una sucursal
	if contar_producto_inicial or bitacora[0].inicial == 0:


		existencia_inicial  = 0
		existencia_productos =[ producto.existencia for producto in  inventario.objects.filter( sucursal__id  = sucursal_id) ]
		existencia_inicial = sum(existencia_productos)

		bitacora.update(inicial = existencia_inicial )


	#entradas en compra factura
	ProductosFactura = FacturaHasProductos.objects.filter( factura__fecha__year = year , factura__fecha__month = month ,
								factura__fecha__day = day , factura__sucursal = sucursal_id , factura__procesado = 1 )

	list_productos_en_factura = [ producto_.cantidad_emitida  for producto_ in  ProductosFactura ]
	list_productos_en_factura = sum(list_productos_en_factura)
	bitacora.update( entrada_compra_factura = list_productos_en_factura )

	entrada_total = bitacora[0].entrada_total +  list_productos_en_factura
	bitacora.update( entrada_total = entrada_total )



	#actualizamos existencia
	update_bitacora_existencias_de_sistema( sucursal_id )


#se actualiza la existencia del sistema con cualquier cambio 
def update_bitacora_existencias_de_sistema(sucursal_id):

		#current time at now
		current_time = timezone.now() - timedelta(hours=5)
		year = current_time.year
		month = current_time.month
		day = current_time.day




		bitacora =  Bitacora.objects.filter( fecha__year = year , fecha__month = month , fecha__day = day , sucursal = sucursal_id )

		existencia_inicial  = 0
		existencia_productos =[ producto.existencia for producto in  inventario.objects.filter( sucursal__id  = sucursal_id) ]
		existencia_inicial = sum(existencia_productos)

		bitacora.update(total_existencia = existencia_inicial )


def update_disponible_fisico_in_bitacora(sucursal):

		sucursal_id = sucursal
		#current time at now
		current_time = timezone.now() - timedelta(hours=5)
		year = current_time.year
		month = current_time.month
		day = current_time.day

		bitacora =  Bitacora.objects.filter( fecha__year = year , fecha__month = month , fecha__day = day , sucursal = sucursal_id )

		existencia_total  = 0
		existencia_productos = [ producto.existencia for producto in  inventario.objects.filter( sucursal__id  = sucursal_id) ]
		existencia_total = sum(existencia_productos)

		bitacora.update(total_existencia = existencia_total )


def calcular_ventas_totales(sucursal):

		sucursal_id = sucursal
		#current time at now
		current_time = timezone.now() - timedelta(hours=5)
		year = current_time.year
		month = current_time.month
		day = current_time.day

		#calcular el total a facturar de ventas
		FacturarVenta_qs =    FacturarVenta.objects.filter ( fecha__year = year , fecha__month = month , fecha__day = day ,  sucursal = sucursal)
		id_venta_facturacion = FacturarVenta_qs.values("id")

		#ventas totales diarias  por sucursal objectos
		ventas_hoy = venta.objects.filter( fecha__year = year , fecha__month = month , fecha__day = day , sucursal = sucursal ).exclude( id__in = id_venta_facturacion )

		ventas_hoy_total = 0

		#ventas totales a publico por sucursal
		ventas_hoy_publico =0

		#ventas totales a mayoreo por sucursal
		ventas_hoy_mayoreo = 0
		for venta_ in ventas_hoy:

			ventas_hoy_total+= venta_.total

			if venta_.total_productos >= MAYOREO_INT:
				ventas_hoy_mayoreo+= venta_.total
			else:
				ventas_hoy_publico+=venta_.total


		ventas_facturas = 0


		for venta_a_facturar in FacturarVenta_qs:
			ventas_facturas	 +=  venta_a_facturar.venta.total

		ventas_hoy_total_con_factura = ventas_hoy_total

		#current time at now
		current_time = timezone.now() - timedelta(hours=5)
		year = current_time.year
		month = current_time.month
		day = current_time.day




		bitacora =  Bitacora.objects.filter( fecha__year = year , fecha__month = month , fecha__day = day , sucursal = sucursal)

		gastos_en_sucursal = GastosSucursal.objects.filter( fecha__year = year , fecha__month = month , fecha__day = day , corte_dia__sucursal = sucursal)

		gastos_list = [ gasto.gastos for gasto in gastos_en_sucursal ]
		_gastos = sum(gastos_list)

		bitacora.update( ventas_publico = ventas_hoy_publico , ventas_mayoreo = ventas_hoy_mayoreo ,
				dep_en_facturas = ventas_facturas , gastos = _gastos , total_a_depositar = ventas_hoy_total)




