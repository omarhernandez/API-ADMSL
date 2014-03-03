from tastypie.api import Api
from apps.api.resource import *

v1_api = Api(api_name='v1')

v1_api.register(UsuarioResource())
v1_api.register(LoginResource())

