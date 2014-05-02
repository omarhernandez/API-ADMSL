from django.db.models import Q , F
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

class ISELAuthentication(Authorization):

	def create_list( self , object_list, bundle):
		raise Unauthorized("sorry, dont create")
		 


	def is_authenticated( self , request , **kwargs ):
		return False

#************************************************************************************************************
#********************************************* Usuario Sucursal *******************************************
#************************************************************************************************************


class UsuarioHasSucursalResource(ModelResource):

	usuario = fields.ForeignKey("apps.api.resource.UsuarioResource", 'usuario'    ,  null = True , full = True )
	Sucursal_id  = fields.ForeignKey("apps.api.resource.SucursalResource", 'Sucursal_id'    ,  null = True ,full = True )

	class Meta:
		queryset = UsuarioHasSucursal.objects.all()
		resource_name ='usuariohassucursal'
		authorization= Authorization()







#************************************************************************************************************
#********************************************* Usuario Sucursal *******************************************
#************************************************************************************************************


class UsuarioSucursalResource(ModelResource):

	usuario = fields.ForeignKey("apps.api.resource.UsuarioResource", 'usuario'    ,  null = True )
	class Meta:
		queryset = UsuarioSucursal.objects.all()
		resource_name ='usuariosucursal'
		authorization= Authorization()


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
		authorization= Authorization()
		filtering = {

			"categoria" : ["exact"],

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
	producto = fields.ForeignKey(ProductoResource, 'producto'     )
	rango = fields.ForeignKey(RangoResource , 'rango'    , full = True , null = True )

	class Meta:
		always_return_data = True
		queryset = producto_has_rango.objects.all()
		resource_name = 'producto_has_rango'
		authorization= Authorization()




#************************************************************************************************************
#*********************************************Sucursal Inventario  ******************************************
#************************************************************************************************************


class InventarioResource(ModelResource):
	""" Inventario de una sucursal."""

	sucursal = fields.ForeignKey(SucursalResource, 'sucursal'     )
	producto = fields.ForeignKey(ProductoResource, 'producto' , full = True     )

	producto_has_rango  = fields.ToManyField('apps.api.resource.ProductoHasRangoesource',  
	 	
			attribute = lambda bundle: producto_has_rango.objects.filter(Q(sucursal = bundle.obj.sucursal) , Q( producto = bundle.obj.producto) )
	  		
		, null = True , full = True		)    



	class Meta:
		queryset = inventario.objects.all()
		always_return_data = True
		resource_name = 'inventario'
		filtering = {
			  	"sucursal" : ["exact"]
			  }
		authorization= Authorization()


class VentaResource(ModelResource):
	""" venta de una sucursal."""

	sucursal = fields.ForeignKey(SucursalResource, 'sucursal'     )
	producto = fields.ToManyField('apps.api.resource.VentaHasProductoResource',  
	 	
			attribute = lambda bundle: venta_has_producto.objects.filter(venta = bundle.obj)
	  		
		, null = True , full = True		)    



	class Meta:
		queryset = venta.objects.all()
		resource_name = 'venta'
		filtering = { "sucursal" : ["exact"] }
		authorization= Authorization()
		always_return_data = True

	def dehydrate(self , bundle):
		#bundle.data["folio"] = bundle.obj.id

		return bundle

	
	def obj_create(self, bundle, request=None, **kwargs): 

		bundle = self.full_hydrate(bundle)
		productos = bundle.data["producto"]
		bundle.obj.save()

		sucursal =   re.search('\/api\/v1\/sucursal\/(\d+)\/', str(bundle.data["sucursal"])).group(1)
		sucursal = Sucursal.objects.filter(id = sucursal)
		for producto in productos:

			id_producto =   re.search('\/api\/v1\/producto\/(\d+)\/', str(producto["producto"])).group(1)
			id_producto = Producto.objects.filter(id = id_producto)[0]

			cantidad = producto["cantidad"]

			
			#decuenta el producto en venta al inventario de la sucursal actual
			inventario.objects.filter ( producto = id_producto , sucursal = sucursal ).update(existencia = F("existencia") - cantidad )

			#guarda los productos dentro de la venta
			venta_has_producto.objects.create( venta = bundle.obj , producto = id_producto , cantidad = cantidad ) 


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
	class Meta:
		queryset = ClienteDatos.objects.all()
		resource_name = 'cliente'
		always_return_data = True
		authorization = Authorization()

		filtering = {

			  "nombre" : ["icontains"],
			  "sucursal" : ["exact"],

			}



#************************************************************************************************************
#*********************************************Cliente Facturacion *******************************************
#************************************************************************************************************


class ClienteFacturacionResource(ModelResource):

	cliente_datos = fields.ForeignKey(ClienteResource, 'cliente_datos'    , full = True , null = True )
	class Meta:
		queryset = ClienteFacturacion.objects.all()
		resource_name = 'clientefacturacion'
		authorization= Authorization()



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

				bundle.data["sucursal"] =  UsuarioHasSucursal.objects.select_related().filter( usuario = user_exist )[0].Sucursal_id.__dict__
				bundle.data["sucursal"].pop("_state")
				bundle.data["sucursal"]["resource_uri"] =   "api/v1/sucursal/{0}/".format(UsuarioSucursalResponse[0].id )
			
	 	
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
				datos = UsuarioSucursal.objects.filter(id = current_obj.id ) [0]

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

	usuario = fields.ForeignKey("apps.api.resource.UsuarioResource", 'usuario'    ,  null = True )
	sucursal  = fields.ForeignKey("apps.api.resource.SucursalResource", 'sucursal'    ,  null = True )
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
	usuario_sucursal = fields.ForeignKey(UsuarioSucursalResource , 'usuario_sucursal' )

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
		filtering = { "sucursal" : ["exact"] }

	def dehydrate(self , bundle):

		id_current_obj = bundle.obj.id
		try:
			VentaUsuarioSucursalQS = VentaUsuarioSucursal.objects.filter( venta__id = id_current_obj)[0]
			bundle.data["vendedor_sucursal"] = VentaUsuarioSucursalQS.nombre_usuario

		except:
			bundle.data["vendedor_sucursal"] = "sin asignar"


		try:
			ClienteVentaQuerySet = VentaCliente.objects.select_related().filter( venta__id  = id_current_obj )[0]
			nombre_cliente = ClienteVentaQuerySet.cliente_datos.nombre
			bundle.data["nombre_comprador"] =  ( nombre_cliente , "publico")[ not nombre_cliente]
		except :
			bundle.data["nombre_comprador"] =  "publico"

		return bundle


