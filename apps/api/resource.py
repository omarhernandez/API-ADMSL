from django.db.models import Q
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
		print "x"
		raise Unauthorized("sorry, dont create")
		 


	def is_authenticated( self , request , **kwargs ):
		print "here" 
		return False


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

#************************************************************************************************************
#*********************************************SUCURSAL ******************************************************
#************************************************************************************************************

class SucursalResource(ModelResource):

	class Meta:
		queryset = Sucursal.objects.all()
		resource_name = 'sucursal'
		authorization= Authorization()


#************************************************************************************************************
#*********************************************Sucursal Inventario  ******************************************
#************************************************************************************************************


class SucursalInventarioResource(ModelResource):

	sucursal = fields.ForeignKey(SucursalResource, 'sucursal'    , full = True , null = True )
	class Meta:
		queryset = SucursalInventario.objects.all()
		resource_name = 'SucursalInventario'
		authorization= Authorization()



#************************************************************************************************************
#*********************************************   Cliente ****************************************************
#************************************************************************************************************


class ClienteResource(ModelResource):

	#cliente_facturacion = fields.ForeignKey(ClienteFacturacionResource , 'cliente_facturacion'    , full = True , null = True )
	sucursal = fields.ForeignKey(SucursalResource , 'sucursal'    , full = True , null = True )
	class Meta:
		queryset = ClienteDatos.objects.all()
		resource_name = 'cliente'
		authorization= Authorization()

		filtering = {

			  "nombre" : ["icontains"],

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
		#allowed_methods = ['get', 'post' , 'delete' , "put"]		
		#excludes = ["password"]
		queryset = Usuario.objects.all().distinct()
		resource_name = 'usuario'
		#authorization= ISELAuthentication()


	def dehydrate(self , bundle ):

		keyword = User.objects.make_random_password()
		bundle.data["loggin"] = keyword
		#del bundle.data["logged"]

		

		return bundle


	def obj_create(self , bundle , request = None , ):
		print bundle.obj

		keyword = User.objects.make_random_password()
		#last_loggin = Logged.objects.create( session_key = keyword , access = True )
		#bundle.obj.logged  = last_loggin

		print bundle.obj.__dict__

		bundle = self.full_hydrate(bundle)
		bundle.obj.save()


		print bundle.obj.__dict__



		#Usuario.objects.update(pk = bundle.obj ).set(logged = last_loggin )


		return bundle





