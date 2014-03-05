from tastypie.api import Api
from apps.api.resource import *

v1_api = Api(api_name='v1')

v1_api.register(UsuarioResource())
v1_api.register(LoginResource())
v1_api.register(ClienteResource())
v1_api.register(SucursalResource())
v1_api.register(ClienteFacturacionResource())
v1_api.register(SucursalInventarioResource())


